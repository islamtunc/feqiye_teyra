# Bismillahirrahmanirrahim
# Elhamdulillahirabbulalemin
# Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
# ALLAH U Teala bizleri bu ilimden faydalandırsın.
# La ilahe illallah, Muhammedun Resulullah.
# SubhanAllahilazim ve bihamdihi, SubhanAllahil azim.
# Allah u Ekber, Allah u Ekber, La ilahe illallah, Allah u Ekber, Allahu Ekber, ve lillahi'l-hamd.
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import os

from api.models.model import SimpleCTCModel, ctc_decode

# 1. Manifest dosyasını oku
manifest_path = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\train_manifest.csv"
with open(manifest_path, "r", encoding="utf-8") as f:
    lines = [line.strip().split("|") for line in f if "|" in line]

print(f"Manifestte {len(lines)} satır var.")
print("İlk 3 satır:", lines[:3])

# 2. Label haritası (örnek)
labels = [
    'a', 'b', 'c', 'ç', 'd', 'e', 'ê', 'f', 'g', 'h', 'i', 'î', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 'ş', 't', 'u', 'û', 'v', 'w', 'x', 'y', 'z', '', 'ع'
]
label2idx = {c: i for i, c in enumerate(labels)}

# 3. Basit bir DataLoader (örnek, tüm veriyi RAM'e alır)
def text_to_indices(text):
    return [label2idx.get(c, 0) for c in text if c in label2idx]

data = []
for npy_path, transcript in lines:
    if not os.path.exists(npy_path):
        print("Eksik dosya:", npy_path)
    features = np.load(npy_path)
    target = text_to_indices(transcript)
    data.append((features, target))

# 4. Model, loss, optimizer
model = SimpleCTCModel(input_dim=80, hidden_dim=128, output_dim=len(labels))
ctc_loss = nn.CTCLoss(blank=labels.index(''), zero_infinity=True)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# 5. Eğitim döngüsü (çok basit, batchsiz)
for epoch in range(10):
    total_loss = 0
    for features, target in data:
        x = torch.tensor(features, dtype=torch.float32).transpose(0, 1).unsqueeze(0)  # [1, time, n_mels]
        x_lens = torch.tensor([x.shape[1]], dtype=torch.int32)
        y = torch.tensor(target, dtype=torch.long).unsqueeze(0)
        y_lens = torch.tensor([len(target)], dtype=torch.int32)

        logits = model(x, x_lens)
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        loss = ctc_loss(log_probs.transpose(0, 1), y, x_lens, y_lens)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Loss: {total_loss/len(data):.4f}")

print("Eğitim tamamlandı!")

# Modeli kaydetmek için:
torch.save(model.state_dict(), "ctc_model.pth")
import os

transcript_path = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\transcripts.txt"
features_dir = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\mmmfeature"
manifest_out = r"C:\Users\admin\Documents\GitHub\feqiye_teyra\api\data\train_manifest.csv"

with open(transcript_path, "r", encoding="utf-8") as fin, open(manifest_out, "w", encoding="utf-8") as fout:
    for line in fin:
        if "|" not in line:
            continue
        fname, text = line.strip().split("|", 1)
        npy_path = os.path.join(features_dir, fname.strip().replace(".wav", ".npy").replace(".opus", ".npy"))
        fout.write(f"{npy_path}|{text.strip()}\n")
