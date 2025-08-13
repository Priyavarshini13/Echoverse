from fastapi import APIRouter, UploadFile, File
import os
from fastapi.responses import JSONResponse
import PyPDF2  # PDF reading


router = APIRouter(prefix="/files", tags=["Files"])

UPLOAD_DIR = "uploads/files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "size": os.path.getsize(file_location)}

