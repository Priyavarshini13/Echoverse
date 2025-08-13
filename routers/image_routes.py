from fastapi import APIRouter, UploadFile, File
import os
from fastapi.responses import JSONResponse
from PIL import Image          # Image processing
import pytesseract            # OCR


router = APIRouter(prefix="/images", tags=["Images"])

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, image.filename)
    with open(file_location, "wb") as f:
        f.write(await image.read())
    return {"filename": image.filename, "size": os.path.getsize(file_location)}



