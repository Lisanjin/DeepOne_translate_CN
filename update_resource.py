"""Patch a DeepOne project.js to load translations from GitHub Pages."""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path


GITHUB_PAGES_BASE = "https://lisanjin.github.io/DeepOne_translate_CN/"
GITHUB_URL_FIELD = "__deeponeModGithubUrl"
FALLBACK_URL_FIELD = "__deeponeModFallbackUrl"
IDENTIFIER = r"[$A-Za-z_][$\w]*"


class PatchError(RuntimeError):
    """Raised when project.js no longer matches the expected structure."""


def _expect_one(
    pattern: re.Pattern[str],
    source: str,
    label: str,
) -> re.Match[str]:
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        raise PatchError(
            f"Expected exactly one {label}, found {len(matches)}. "
            "The upstream project.js format may have changed."
        )
    return matches[0]


def _method_bounds(
    source: str,
    method_name: str,
    next_method_name: str,
) -> tuple[int, int]:
    start_pattern = re.compile(
        rf"{re.escape(method_name)}\s*:\s*function\s*\("
    )
    start = _expect_one(start_pattern, source, method_name).start()
    end_pattern = re.compile(
        rf",\s*{re.escape(next_method_name)}\s*:\s*function\s*\("
    )
    end_match = end_pattern.search(source, start)
    if end_match is None:
        raise PatchError(
            f"Could not find {next_method_name} after {method_name}."
        )
    return start, end_match.start()


def _patch_load_adv(source: str) -> str:
    start, end = _method_bounds(source, "loadAdvFileEx", "loadFileExInner")
    method = source[start:end]

    header_pattern = re.compile(
        rf"loadAdvFileEx\s*:\s*function\s*\("
        rf"(?P<name>{IDENTIFIER})\s*,\s*"
        rf"(?P<path>{IDENTIFIER})\s*,\s*"
        rf"(?P<md5>{IDENTIFIER})\s*,\s*"
        rf"(?P<callback>{IDENTIFIER})\s*\)\s*\{{"
    )
    header = _expect_one(header_pattern, method, "loadAdvFileEx header")
    name_var = header.group("name")
    md5_var = header.group("md5")

    call_pattern = re.compile(
        rf"this\.loadFileExInner\(\s*{re.escape(name_var)}\s*,\s*"
        rf"(?P<file_type>{IDENTIFIER})\s*,\s*"
        rf"(?P<remote_url>{IDENTIFIER})\s*,\s*"
        rf"{re.escape(md5_var)}\s*,"
    )
    call = _expect_one(call_pattern, method, "ADV loadFileExInner call")
    remote_url_var = call.group("remote_url")
    github_base_literal = json.dumps(GITHUB_PAGES_BASE, ensure_ascii=True)

    injection = (
        f"this.{GITHUB_URL_FIELD}=null,"
        f"this.{FALLBACK_URL_FIELD}=null;"
        f'if({name_var}.startsWith("download/adv/text/")){{'
        f"this.{FALLBACK_URL_FIELD}={remote_url_var};"
        f"this.{GITHUB_URL_FIELD}={github_base_literal}+{name_var};"
        f"{remote_url_var}=this.{GITHUB_URL_FIELD};"
        "}"
    )
    patched_method = method[: call.start()] + injection + method[call.start() :]
    return source[:start] + patched_method + source[end:]


def _patch_load_file_inner(source: str) -> str:
    start, end = _method_bounds(source, "loadFileExInner", "retry")
    method = source[start:end]

    header_pattern = re.compile(
        rf"loadFileExInner\s*:\s*function\s*\("
        rf"(?P<logical_name>{IDENTIFIER})\s*,\s*"
        rf"(?P<file_type>{IDENTIFIER})\s*,\s*"
        rf"(?P<remote_arg>{IDENTIFIER})\s*,\s*"
        rf"(?P<md5>{IDENTIFIER})\s*,\s*"
        rf"(?P<callback>{IDENTIFIER})\s*\)\s*\{{\s*"
        rf"var\s+(?P<self>{IDENTIFIER})\s*=\s*this\s*,"
    )
    header = _expect_one(header_pattern, method, "loadFileExInner header")
    self_var = header.group("self")

    web_load_pattern = re.compile(
        rf"(?P<prefix>cc\.loader\.load\("
        rf"(?P<active_url>{IDENTIFIER})\s*,\s*"
        rf"function\s+(?P<retry_func>{IDENTIFIER})\("
        rf"(?P<error>{IDENTIFIER})\s*,\s*"
        rf"(?P<content>{IDENTIFIER})\)\s*\{{)"
        rf"\s*if\s*\(\s*(?P=error)\s*\)"
    )
    web_load = _expect_one(
        web_load_pattern,
        method,
        "Web cc.loader.load handler",
    )
    active_url_var = web_load.group("active_url")
    retry_func_var = web_load.group("retry_func")
    error_var = web_load.group("error")
    web_fallback = (
        web_load.group("prefix")
        + f"if({error_var}&&"
        + f"{active_url_var}==={self_var}.{GITHUB_URL_FIELD}&&"
        + f"{self_var}.{FALLBACK_URL_FIELD}){{"
        + f"{active_url_var}={self_var}.{FALLBACK_URL_FIELD},"
        + f"{self_var}.{FALLBACK_URL_FIELD}=null;"
        + f"return void cc.loader.load({active_url_var},{retry_func_var});"
        + "}"
        + f"if({error_var})"
    )
    method = (
        method[: web_load.start()]
        + web_fallback
        + method[web_load.end() :]
    )

    native_retry_pattern = re.compile(
        rf"{re.escape(self_var)}\.downloader\.createDownloadFileTask\("
        rf"(?P<active_url>{IDENTIFIER})\s*,\s*"
        rf"(?P<local_path>{IDENTIFIER})\)"
    )
    native_retry = _expect_one(
        native_retry_pattern,
        method,
        "native downloader retry call",
    )
    native_url_var = native_retry.group("active_url")
    local_path_var = native_retry.group("local_path")

    native_error_pattern = re.compile(
        rf"(?P<prefix>this\.downloader\.setOnTaskError\(function\("
        rf"{IDENTIFIER}\s*,\s*{IDENTIFIER}\s*,\s*"
        rf"{IDENTIFIER}\s*,\s*{IDENTIFIER}\)\s*\{{)"
    )
    native_error = _expect_one(
        native_error_pattern,
        method,
        "native downloader error handler",
    )
    native_fallback = (
        native_error.group("prefix")
        + f"if({native_url_var}==={self_var}.{GITHUB_URL_FIELD}&&"
        + f"{self_var}.{FALLBACK_URL_FIELD}){{"
        + f"{native_url_var}={self_var}.{FALLBACK_URL_FIELD},"
        + f"{self_var}.{FALLBACK_URL_FIELD}=null,"
        + f"{self_var}.curDownLoadTime=1;"
        + f"return void {self_var}.downloader.createDownloadFileTask("
        + f"{native_url_var},{local_path_var});"
        + "}"
    )
    method = (
        method[: native_error.start()]
        + native_fallback
        + method[native_error.end() :]
    )
    return source[:start] + method + source[end:]


def _patch_native_adv_update_check(source: str) -> str:
    pattern = re.compile(
        rf"var\s+(?P<result>{IDENTIFIER})\s*=\s*"
        rf"this\.isResNeedUpdate\("
        rf"(?P<storage>{IDENTIFIER})\s*,\s*"
        rf"(?P<normal_storage>{IDENTIFIER})\s*,\s*"
        rf"(?P<name>{IDENTIFIER})\s*,\s*"
        rf"(?P<md5>{IDENTIFIER})\s*\);"
    )
    match = _expect_one(pattern, source, "isResNeedUpdate call")
    result_var = match.group("result")
    name_var = match.group("name")
    injection = (
        match.group(0)
        + f'if({name_var}.startsWith("adv/text/")){{'
        + f"{result_var}.need=true;"
        + "}"
    )
    return source[: match.start()] + injection + source[match.end() :]


def _patch_project_js(source: str) -> str:
    if GITHUB_URL_FIELD in source or FALLBACK_URL_FIELD in source:
        raise PatchError("project.js already contains the direct-CDN patch")

    patched = _patch_load_adv(source)
    patched = _patch_load_file_inner(patched)
    patched = _patch_native_adv_update_check(patched)

    if patched.count(GITHUB_PAGES_BASE) != 1:
        raise PatchError("GitHub Pages URL was not injected exactly once")
    if patched.count(GITHUB_URL_FIELD) < 4:
        raise PatchError("Direct-CDN patch validation failed")

    return patched


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as file:
            file.write(data)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def _patch_comment(original: bytes) -> str:
    patch_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    original_md5 = hashlib.md5(original).hexdigest()
    return (
        f"// patch_data: {patch_time}"
        f"\n// md5:{original_md5}"
        "\n// [Lisanjin/DeepOne_translate_CN]"
        "(https://github.com/Lisanjin/DeepOne_translate_CN)\n"
    )


def update(
    input_path: str | os.PathLike[str],
    output_path: str | os.PathLike[str],
) -> bool:
    """Atomically write a patched copy; return False if only its date differs."""

    input_file = Path(input_path).resolve(strict=True)
    output_file = Path(output_path).resolve(strict=False)
    if input_file == output_file:
        raise ValueError("input_path and output_path must be different files")

    source_bytes = input_file.read_bytes()
    try:
        source = source_bytes.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ValueError(f"{input_file} is not valid UTF-8") from error

    patched = (_patch_comment(source_bytes) + _patch_project_js(source)).encode(
        "utf-8"
    )
    # The first line contains the patch time, not a change to the game script.
    # Compare the remaining metadata and code so repeated runs stay unchanged.
    if output_file.is_file():
        current = output_file.read_bytes()
        if current.partition(b"\n")[2] == patched.partition(b"\n")[2]:
            return False
    _atomic_write(output_file, patched)
    return True

if __name__ == "__main__":
    update("project.js", "project_patched.js")
