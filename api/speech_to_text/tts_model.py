"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
"""
PyTorch tabanlı basit bir TTS (Text-to-Speech) model iskeleti.
Bu dosya, kendi TTS modelinizi geliştirmek için temel bir başlangıç sunar.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleTTSModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim=256, hidden_dim=512, mel_dim=80, num_layers=2):
        super(SimpleTTSModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.encoder = nn.LSTM(embedding_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=True)
        self.decoder = nn.LSTM(hidden_dim*2, hidden_dim, num_layers=num_layers, batch_first=True)
        self.mel_linear = nn.Linear(hidden_dim, mel_dim)
    def forward(self, text, text_lengths):
        # text: [batch, seq]
        embedded = self.embedding(text)
        packed = nn.utils.rnn.pack_padded_sequence(embedded, text_lengths, batch_first=True, enforce_sorted=False)
        enc_out, _ = self.encoder(packed)
        enc_out, _ = nn.utils.rnn.pad_packed_sequence(enc_out, batch_first=True)
        dec_out, _ = self.decoder(enc_out)
        mel_out = self.mel_linear(dec_out)
        return mel_out  # [batch, seq, mel_dim]

# Kullanım örneği:
# model = SimpleTTSModel(vocab_size=..., mel_dim=80)
# text = torch.randint(0, vocab_size, (batch_size, seq_len))
# text_lengths = torch.full((batch_size,), seq_len, dtype=torch.long)
# mel = model(text, text_lengths)
