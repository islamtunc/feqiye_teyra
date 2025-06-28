"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
"""
Basit bir LLM (Large Language Model) iskeleti.
PyTorch tabanlı, karakter seviyesinde çalışan küçük bir Transformer dil modeli örneği.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from .tokenizer import SimpleTokenizer

class SimpleCharTransformerLM(nn.Module):
    def __init__(self, vocab_size, d_model=128, nhead=4, num_layers=2, dim_feedforward=256, max_len=256):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.pos_embedding = nn.Embedding(max_len, d_model)
        encoder_layer = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)
        self.fc = nn.Linear(d_model, vocab_size)
        self.max_len = max_len
    def forward(self, x):
        # x: [batch, seq]
        positions = torch.arange(0, x.size(1), device=x.device).unsqueeze(0)
        x = self.embedding(x) + self.pos_embedding(positions)
        x = x.transpose(0, 1)  # Transformer expects [seq, batch, d_model]
        x = self.transformer(x)
        x = x.transpose(0, 1)
        logits = self.fc(x)
        return logits  # [batch, seq, vocab_size]

def train_llm_on_txt(txt_path, model_save_path=None, epochs=3, seq_len=128, batch_size=32, lr=1e-3, device='cpu'):
    # 1. Veriyi oku
    with open(txt_path, encoding='utf-8') as f:
        text = f.read()
    # 2. Tokenizer ve vocab
    tokenizer = SimpleTokenizer()
    tokenizer.fit([text])
    vocab_size = len(tokenizer.vocab)
    # 3. Veriyi encode et
    encoded = tokenizer.encode(text)
    # 4. Dataset hazırla (karakter dil modeli, next token prediction)
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, Dataset
    class CharDataset(Dataset):
        def __init__(self, data, seq_len):
            self.data = data
            self.seq_len = seq_len
        def __len__(self):
            return len(self.data) - self.seq_len
        def __getitem__(self, idx):
            x = self.data[idx:idx+self.seq_len]
            y = self.data[idx+1:idx+self.seq_len+1]
            return torch.tensor(x), torch.tensor(y)
    ds = CharDataset(encoded, seq_len)
    dl = DataLoader(ds, batch_size=batch_size, shuffle=True)
    # 5. Model
    model = SimpleCharTransformerLM(vocab_size=vocab_size, max_len=seq_len).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.CrossEntropyLoss()
    # 6. Eğitim döngüsü
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for xb, yb in dl:
            xb, yb = xb.to(device), yb.to(device)
            logits = model(xb)
            loss = loss_fn(logits.view(-1, vocab_size), yb.view(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        print(f"Epoch {epoch+1}/{epochs} - Loss: {total_loss/len(dl):.4f}")
    # 7. Modeli kaydet
    if model_save_path:
        torch.save({'model': model.state_dict(), 'vocab': tokenizer.vocab}, model_save_path)
        print(f"Model kaydedildi: {model_save_path}")
    return model, tokenizer

# Kullanım örneği:
# model = SimpleCharTransformerLM(vocab_size=..., max_len=256)
# x = torch.randint(0, vocab_size, (batch_size, seq_len))
# logits = model(x)
# train_llm_on_txt('c:/Users/admin/feqi/Feqi/data/mm.txt', 'llm_model.pth', device='cuda')
