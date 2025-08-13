from fastapi import APIRouter, UploadFile, File
import os
from fastapi.responses import JSONResponse
import speech_recognition as sr


router = APIRouter(prefix="/voice", tags=["Voice"])

UPLOAD_DIR = "uploads/voice"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_voice(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "size": os.path.getsize(file_location)}

