"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
"""
Speech-to-Text Pipeline (PyTorch, CTC, Mel Spectrogram)
Bu modül, mevcut ASR projenizle uyumlu şekilde ses dosyasını metne çevirir.
"""
import torch
from models.model import SimpleCTCModel, ctc_decode
from asr.preprocess import preprocess_audio

class SpeechToText:
    def __init__(self, model, labels, device='cpu'):
        self.model = model.to(device)
        self.labels = labels
        self.device = device
    def transcribe(self, audio_path):
        features = preprocess_audio(audio_path)
        features = torch.tensor(features, dtype=torch.float32).transpose(0, 1).unsqueeze(0)  # [1, time, n_mels]
        input_lengths = torch.tensor([features.shape[1]], dtype=torch.int32)
        features = features.to(self.device)
        input_lengths = input_lengths.to(self.device)
        self.model.eval()
        with torch.no_grad():
            logits = self.model(features, input_lengths)
            log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
        text = ctc_decode(log_probs, self.labels)[0]
        return text

# Kullanım örneği:
# labels = ['a', 'b', 'c', ..., ' ']
# model = SimpleCTCModel(input_dim=80, hidden_dim=128, output_dim=len(labels))
# stt = SpeechToText(model, labels)
# print(stt.transcribe('path/to/audio.wav'))
