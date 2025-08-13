import os
import pytesseract
from PIL import Image
from werkzeug.utils import secure_filename

def process_image_ocr(image):
    filename = secure_filename(image.filename)
    path = os.path.join("uploads/images", filename)
    image.save(path)
    text = pytesseract.image_to_string(Image.open(path))
    return {"status": "success", "text": text}
