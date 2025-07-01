"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Allah'tan başka ilah yoktur, Muhammed (s.a.v) O'nun Resulüdür.
   SubhanAllahilazim ve bihamdihi, SubhanAllahil azim.
   Amin.
"""
import os
import csv
from api.asr.preprocess import preprocess_audio
import numpy as np

# Klasör ve dosya yolları
AUDIO_DIR = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\mmmdeng"
TRANSCRIPT_PATH = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\transcripts.txt"
FEATURES_DIR = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\mmmfeature"
CSV_OUT = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\train_manifest.csv"

os.makedirs(FEATURES_DIR, exist_ok=True)

# 1. Transkriptleri oku ve tekrarsız bir sözlük oluştur
transcript_dict = {}
with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if "|" not in line:
            continue
        fname, text = line.strip().split("|", 1)
        fname = fname.strip()
        if fname not in transcript_dict:  # Tekrarlı dosya adını atla
            transcript_dict[fname] = text.strip()

# 2. Ses dosyalarını işle, Mel Spectrogram çıkar, .npy olarak kaydet ve manifest oluştur
with open(CSV_OUT, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["feature_path", "transcript"])
    seen = set()
    for fname in os.listdir(AUDIO_DIR):
        if not fname.endswith(".wav"):
            continue
        fname_clean = fname.strip()
        if fname_clean in seen:
            continue
        seen.add(fname_clean)
        audio_path = os.path.join(AUDIO_DIR, fname_clean)
        mel = preprocess_audio(audio_path)
        feature_path = os.path.join(FEATURES_DIR, fname_clean.replace(".wav", ".npy"))
        np.save(feature_path, mel)
        transcript = transcript_dict.get(fname_clean, "")
        writer.writerow([feature_path, transcript])

print("Tüm ön işleme ve manifest oluşturma işlemi tamamlandı! (Tekrarsız)")
