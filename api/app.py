#Bismillahirrahmanirahim
#Elhamdulillahirabbulalemin
# Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ve sahbihi ecmain
# Allah u Ekber velillahilhamd
# La ilahe illallah Muhammedur Rasulullah
# SuphanAllahilazim ve bihamdihi
# La havle ve la kuvvete illa billahil aliyyil azim
# Hasbunallahu ve ni'mel vekil


"""
FastAPI tabanlı bir backend uygulaması.
Bu dosya, feqi modülü altında API sunar ve Next.js frontend ile kolayca entegre edilebilir.
"""
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os
from speech_to_text.speech_to_text import transcribe_audio  # örnek import
from nlp.llm import get_ai_reply  # örnek import
from speech_to_text.text_to_speech import synthesize_speech  # örnek import

app = FastAPI()

# CORS ayarları (Next.js ile bağlantı için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse sadece Next.js domainini ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "Feqi API çalışıyor!"}

@app.post("/asr/")
def asr_endpoint(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    result = transcribe_audio(file_path)  # kendi fonksiyonunuz
    return JSONResponse({"transcript": result})

@app.post("/message/")
async def message_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    response = get_ai_reply(user_message)  # kendi fonksiyonunuz
    return JSONResponse({"reply": response})

@app.post("/speak/")
async def speak_endpoint(request: Request):
    data = await request.json()
    text = data.get("text", "")
    audio_path = synthesize_speech(text)  # kendi fonksiyonunuz
    return FileResponse(audio_path, media_type="audio/wav")

