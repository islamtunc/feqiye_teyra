"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""

import os
import torch
import torchaudio
from torch import nn
from torch.utils.data import Dataset, DataLoader
import pandas as pd
import numpy as np

# --- Config ---
MANIFEST_PATH = "../data/train_manifest.csv"
BATCH_SIZE = 16
EPOCHS = 10
LEARNING_RATE = 1e-3
MODEL_SAVE_PATH = "../models/asr_model.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- Dataset ---
class ASRDataset(Dataset):
    def __init__(self, manifest_path):
        self.df = pd.read_csv(manifest_path)
        self.feature_paths = self.df['feature_path'].tolist()
        self.transcripts = self.df['transcript'].tolist()
        # Tokenizer: karakter tabanlı
        self.vocab = sorted(list({c for t in self.transcripts for c in t}))
        self.char2idx = {c: i+1 for i, c in enumerate(self.vocab)}  # 0: blank
        self.idx2char = {i+1: c for i, c in enumerate(self.vocab)}
        self.blank_idx = 0

    def __len__(self):
        return len(self.feature_paths)

    def __getitem__(self, idx):
        feature = np.load(self.feature_paths[idx])
        feature = torch.tensor(feature, dtype=torch.float32)
        transcript = self.transcripts[idx]
        target = torch.tensor([self.char2idx[c] for c in transcript], dtype=torch.long)
        return feature, target

    def get_vocab_size(self):
        return len(self.vocab) + 1  # +1 for blank

# --- Collate Function for Padding ---
def collate_fn(batch):
    features, targets = zip(*batch)
    # Pad features (time, mel)
    feature_lengths = [f.shape[0] for f in features]
    max_feat_len = max(feature_lengths)
    feat_dim = features[0].shape[1]
    padded_features = torch.zeros(len(features), max_feat_len, feat_dim)
    for i, f in enumerate(features):
        padded_features[i, :f.shape[0], :] = f
    # Pad targets
    target_lengths = [t.shape[0] for t in targets]
    max_tgt_len = max(target_lengths)
    padded_targets = torch.full((len(targets), max_tgt_len), 0, dtype=torch.long)
    for i, t in enumerate(targets):
        padded_targets[i, :t.shape[0]] = t
    return padded_features, padded_targets, feature_lengths, target_lengths

# --- Model ---
def get_asr_model(input_dim, output_dim):
    return nn.Sequential(
        nn.Linear(input_dim, 256),
        nn.ReLU(),
        nn.Linear(256, output_dim)
    )

# --- Training Loop ---
def train(model, dataloader, criterion, optimizer, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_loss = 0
        for features, targets, feat_lens, tgt_lens in dataloader:
            features = features.to(DEVICE)
            targets = targets.to(DEVICE)
            # Flatten features for simple model: (B, T, F) -> (B*T, F)
            B, T, F = features.shape
            features_flat = features.view(B*T, F)
            logits = model(features_flat)  # (B*T, output_dim)
            logits = logits.view(B, T, -1)  # (B, T, output_dim)
            # CTC Loss expects (T, B, C)
            logits = logits.permute(1, 0, 2)
            # Prepare target for CTC
            target_flat = []
            for i, l in enumerate(tgt_lens):
                target_flat.extend(targets[i, :l].tolist())
            target_flat = torch.tensor(target_flat, dtype=torch.long).to(DEVICE)
            input_lengths = torch.tensor(feat_lens, dtype=torch.long)
            target_lengths = torch.tensor(tgt_lens, dtype=torch.long)
            loss = criterion(logits, target_flat, input_lengths, target_lengths)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(dataloader):.4f}")
    print("Training complete.")

if __name__ == "__main__":
    # Prepare dataset & dataloader
    dataset = ASRDataset(MANIFEST_PATH)
    input_dim = np.load(dataset.feature_paths[0]).shape[1]
    output_dim = dataset.get_vocab_size()
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    # Model, loss, optimizer
    model = get_asr_model(input_dim, output_dim).to(DEVICE)
    criterion = nn.CTCLoss(blank=0, zero_infinity=True)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    # Train
    train(model, dataloader, criterion, optimizer, epochs=EPOCHS)
    # Save model
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    torch.save(model.state_dict(), MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")
