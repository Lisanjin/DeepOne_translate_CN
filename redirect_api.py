from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware  
import os
import uvicorn

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/{file_path:path}")
async def download_file(file_path: str):
    base_dir = os.path.abspath("./")
    full_path = os.path.abspath(os.path.join(base_dir, file_path))
    if os.path.commonpath([base_dir, full_path]) != base_dir:
        return {"error": "File not found"}
    if not os.path.exists(full_path):
        return {"error": "File not found"}
    with open(full_path, "rb") as file: 
        file_content = file.read()
        
    return Response(content=file_content)

if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)