import requests
import json
import os
import hashlib
import concurrent.futures
from urllib.request import urlretrieve

def download_file(url, filename):

    print(f'Downloading {filename}...')
    if os.path.exists(filename):
        print(f'{filename} 已下载，跳过.')
        return
    download_times = 5
    while download_times > 0:
        try:
            directory = filename.replace(filename.split('/')[-1], '')
            if not os.path.exists(directory):
                os.makedirs(directory)
            urlretrieve(url, filename)
        except Exception as e:
            print(e)
            print("error downloading : " + filename)
            download_times = download_times - 1
            continue
        else:
            break
    print(f'{filename} downloaded.')
    


def md5_file(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def get_files_md5(root_folder):
    file_md5_dict = {}
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_md5 = md5_file(file_path)
            file_md5_dict[file_path] = file_md5
    return file_md5_dict

def update_md5():
    print("更新md5字典")
    root_folder = "download"
    file_md5_dict = get_files_md5(root_folder)
    with open("md5.json", 'w', encoding='utf8') as f:
        json.dump(file_md5_dict, f, ensure_ascii=False, indent=4)

def dl_new_files(Redirector):
    print("开始下载新文件……")
    update_list = []
    for redirects in Redirector["redirects"]:
        # "redirectUrl": "http://127.0.0.1:8000/download/adv/text/quest/10001/100101001.txt",
        local_file_path = redirects["redirectUrl"].replace(local_host, "")
        if os.path.exists(local_file_path):
            pass
        else:
            update_list.append(local_file_path)
    
    print("新增剧本数：",len(update_list))
    dl_dir={}
    for local_file_path in update_list:
        dl_url = server_host + local_file_path
        dl_dir[dl_url] = local_file_path
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_file, url, filename) for url, filename in dl_dir.items()]
        
print("准备更新…………")
print("开始检查新剧本…………")
server_host = "http://121.37.154.43:8000/"
local_host = "http://127.0.0.1:8000/"

Redirector_url = server_host + "Redirector.json"
response = requests.get(Redirector_url)
new_Redirector = json.loads(response.text)
with open("Redirector.json", "r", encoding='utf8') as f:
    old_Redirector = json.load(f)

if new_Redirector != old_Redirector:
    print("更新Redirector.json中……")
    with open("Redirector.json", 'w', encoding='utf8') as f:
        json.dump(new_Redirector, f, ensure_ascii=False, indent=4)
else:
    print("无新剧本")
    
dl_new_files(new_Redirector)
#——————————————————————————————————————————————————————

md5_url = server_host +"md5.json"
def update_old_files():
    response = requests.get(md5_url)
    new_md5 = json.loads(response.text)

    with open("md5.json", "r", encoding='utf8') as f:
        old_md5 = json.load(f)

    update_list = []

    if new_md5 != old_md5:
        print("检查到md5变动")
        for k,v in old_md5.items():
            if v != new_md5[k]:
                update_list.append(k.replace("\\","/"))
    
    print("变动剧本数：",len(update_list))
    dl_dir={}
    for local_file_path in update_list:
        dl_url = server_host + local_file_path
        dl_dir[dl_url] = local_file_path
        os.remove(local_file_path)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(download_file, url, filename) for url, filename in dl_dir.items()]

update_old_files()
update_md5()