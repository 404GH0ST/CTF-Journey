from fastapi.responses import HTMLResponse
from pathlib import Path
from fastapi import UploadFile, APIRouter,Request, HTTPException
import uuid
import os
import json
from PyPDF2 import PdfReader
from subprocess import run, CalledProcessError

app = APIRouter()
UPLOAD_PATH = Path("./uploads/")

    
@app.post("/upload")
async def upload(file: UploadFile):
    try:
        file_path = UPLOAD_PATH / f"{uuid.uuid4()}.pdf" 
        contents = file.file.read()
        print(contents)
        with open(file_path, "wb") as f:
            f.write(contents)
    except Exception as e:
        return {"message": "There was an error uploading the file : "+ str(e)}
    return {
        "message": "File uploaded successfully.",
        "file_path": str(file_path)
    }



@app.get("/logger")
async def log(request: Request):
    url_to_visit = request.query_params.get('url')
    if not url_to_visit.startswith(str(request.base_url) + 'view'):
        print(str(request.base_url) + '/view')
        raise HTTPException(status_code=400, detail='Invalid URL format')
    
    command = ["node", "./bot.js", json.dumps({"url": url_to_visit, "token": os.environ.get('FLAG') or 'fake_token'})]
    try:
        completed_process = run(command, check=True, capture_output=True, text=True)
    except CalledProcessError as e:
        print("An error occurred:", e)
        print("Standard output:", e.stdout)
        print("Standard error:", e.stderr)
        raise HTTPException(status_code=500, detail='Internal server error')
    
    return 'Logged...'

@app.get("/view/{filename}")
async def view(filename: str):
    file_path = UPLOAD_PATH / filename
    if not file_path.exists():
        return {"error": "File not found."}
    #     REDACTED_CODE_ENUM_FIRST
    return HTMLResponse(content=html_content, status_code=200)