"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Allah'tan başka ilah yoktur, Muhammed (s.a.v) O'nun Resulüdür.
   SubhanAllahilazim ve bihamdihi, SubhanAllahil azim.
   Amin.
"""

import os
import glob
import csv
from preprocess import preprocess_audio
import numpy as np

# 1. Ses dosyalarının ve transkriptlerin olduğu klasörleri belirt
AUDIO_DIR = "../../data"  # Ses dosyalarının olduğu klasör
TRANSCRIPT_PATH = "../../data/transcripts.txt"  # Her satır: dosya_adı.wav|transkript
FEATURES_DIR = "../../features"  # Mel spectrogramların kaydedileceği klasör
CSV_OUT = "../../train_manifest.csv"  # Model eğitimi için CSV

os.makedirs(FEATURES_DIR, exist_ok=True)

# 2. Transkriptleri oku
transcript_dict = {}
with open(TRANSCRIPT_PATH, "r", encoding="utf-8") as f:
    for line in f:
        fname, text = line.strip().split("|", 1)
        transcript_dict[fname] = text

# 3. Ses dosyalarını işle ve CSV oluştur
with open(CSV_OUT, "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["feature_path", "transcript"])
    for fname in os.listdir(AUDIO_DIR):
        if not fname.endswith(".wav"):
            continue
        audio_path = os.path.join(AUDIO_DIR, fname)
        mel = preprocess_audio(audio_path)
        feature_path = os.path.join(FEATURES_DIR, fname.replace(".wav", ".npy"))
        np.save(feature_path, mel)
        transcript = transcript_dict.get(fname, "")
        writer.writerow([feature_path, transcript])

print("ASR veri hazırlama tamamlandı!")
