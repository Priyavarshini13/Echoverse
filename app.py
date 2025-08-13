# app.py
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import date

# File processing
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
import pytesseract
import speech_recognition as sr
from pydub import AudioSegment

# ---------------------------
# Directories
# ---------------------------
UPLOAD_DIR = "uploads"
FILE_DIR = os.path.join(UPLOAD_DIR, "files")
IMAGE_DIR = os.path.join(UPLOAD_DIR, "images")
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")

os.makedirs(FILE_DIR, exist_ok=True)
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# ---------------------------
# FastAPI app
# ---------------------------
app = FastAPI(title="EchoVerse Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------
# SQLite setup
# ---------------------------
conn = sqlite3.connect("usage.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    feature TEXT,
    user_id TEXT,
    is_premium INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    is_premium INTEGER DEFAULT 0
)
""")
conn.commit()

# ---------------------------
# Configuration
# ---------------------------
FREE_LIMITS = {
    "text_input": 5,
    "file_upload": 3,
    "image_upload": 3,
    "voice_upload": 2
}

# ---------------------------
# Helper Functions
# ---------------------------
def is_premium(user_id: str) -> bool:
    cursor.execute("SELECT is_premium FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row[0] == 1 if row else False

def log_usage(user_id: str, feature: str):
    premium = 1 if is_premium(user_id) else 0
    cursor.execute("INSERT INTO usage (feature, user_id, is_premium) VALUES (?, ?, ?)",
                   (feature, user_id, premium))
    conn.commit()

def check_limit(user_id: str, feature: str):
    if is_premium(user_id):
        return
    today = date.today().isoformat()
    cursor.execute(
        "SELECT COUNT(*) FROM usage WHERE user_id=? AND feature=? AND DATE(timestamp)=?",
        (user_id, feature, today)
    )
    count = cursor.fetchone()[0]
    if count >= FREE_LIMITS.get(feature, 0):
        raise HTTPException(status_code=403, detail=f"Free limit reached for {feature}")

def extract_pdf_text(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_docx_text(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_txt_text(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_image_text(file_path):
    img = Image.open(file_path)
    return pytesseract.image_to_string(img)

def transcribe_audio(file_path):
    r = sr.Recognizer()
    if not file_path.endswith(".wav"):
        sound = AudioSegment.from_file(file_path)
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        sound.export(wav_path, format="wav")
        file_path = wav_path
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    return r.recognize_google(audio)

# ---------------------------
# Routes
# ---------------------------
@app.get("/")
def root():
    return {"message": "EchoVerse Backend is running!"}

# ---- User registration ----
@app.post("/register")
def register_user(user_id: str = Form(...), is_premium: int = Form(0)):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, is_premium) VALUES (?, ?)", (user_id, is_premium))
    conn.commit()
    return {"message": f"User {user_id} registered", "is_premium": bool(is_premium)}

# ---- Text Input ----
@app.post("/text")
def receive_text(user_id: str = Form(...), text: str = Form(...)):
    check_limit(user_id, "text_input")
    log_usage(user_id, "text_input")
    return {"status": "success", "text": text}

# ---- File Upload (PDF/DOCX/TXT) ----
@app.post("/upload/file")
async def upload_file(user_id: str = Form(...), file: UploadFile = File(...)):
    check_limit(user_id, "file_upload")
    file_path = os.path.join(FILE_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    if file.filename.endswith(".pdf"):
        extracted_text = extract_pdf_text(file_path)
    elif file.filename.endswith(".docx"):
        extracted_text = extract_docx_text(file_path)
    elif file.filename.endswith(".txt"):
        extracted_text = extract_txt_text(file_path)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

    log_usage(user_id, "file_upload")
    return {"filename": file.filename, "extracted_text": extracted_text}

# ---- Image Upload + OCR ----
@app.post("/upload/image")
async def upload_image(user_id: str = Form(...), image: UploadFile = File(...)):
    check_limit(user_id, "image_upload")
    image_path = os.path.join(IMAGE_DIR, image.filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    extracted_text = extract_image_text(image_path)
    log_usage(user_id, "image_upload")
    return {"filename": image.filename, "extracted_text": extracted_text}

# ---- Voice Upload + Transcription ----
@app.post("/upload/voice")
async def upload_voice(user_id: str = Form(...), audio: UploadFile = File(...)):
    check_limit(user_id, "voice_upload")
    audio_path = os.path.join(AUDIO_DIR, audio.filename)
    with open(audio_path, "wb") as f:
        f.write(await audio.read())

    transcription = transcribe_audio(audio_path)
    log_usage(user_id, "voice_upload")
    return {"filename": audio.filename, "transcription": transcription}

# ---- Download Files ----
@app.get("/download/{folder}/{filename}")
def download_file(folder: str, filename: str):
    folder_map = {"files": FILE_DIR, "images": IMAGE_DIR, "audio": AUDIO_DIR}
    if folder not in folder_map:
        raise HTTPException(status_code=400, detail="Invalid folder")
    file_path = os.path.join(folder_map[folder], filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)
