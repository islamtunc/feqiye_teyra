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
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import os

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
    # Burada ASR modelini çağırıp sonucu alın (örnek çıktı):
    # result = transcribe(file_path, model, labels)
    result = "(örnek çıktı) Ses başarıyla işlendi."
    return JSONResponse({"transcript": result})

