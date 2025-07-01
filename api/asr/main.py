"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Allah'tan başka ilah yoktur, Muhammed (s.a.v) O'nun Resulüdür.
   SubhanAllahilazim ve bihamdihi, SubhanAllahil azim.
   Amin.
"""

import torch
import torchaudio
from models.model import SimpleCTCModel, ctc_decode
from preprocess import preprocess_audio

def transcribe(audio_path, model, labels, device='cpu'):
    """
    Loads audio, extracts features, runs model, and decodes output to text.
    """
    # Preprocess audio
    features = preprocess_audio(audio_path)
    features = torch.tensor(features, dtype=torch.float32).transpose(0, 1).unsqueeze(0)  # [1, time, n_mels]
    input_lengths = torch.tensor([features.shape[1]], dtype=torch.int32)
    features = features.to(device)
    input_lengths = input_lengths.to(device)
    model.eval()
    with torch.no_grad():
        logits = model(features, input_lengths)  # [1, time, classes]
        log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
    text = ctc_decode(log_probs, labels)[0]
    return text

def main():
    print('PyTorch version:', torch.__version__)
    print('Torchaudio version:', torchaudio.__version__)
    print('ASR project setup is ready!')
    # Example usage
    labels = [
        'a', 'b', 'c', 'ç', 'd', 'e', 'ê', 'f', 'g', 'h', 'i', 'î', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 'ş', 't', 'u', 'û', 'v', 'w', 'x', 'y', 'z', '', 'ع'
    ]  # Kürtçe harfler, boşluk ve Arapça 'ayn' harfi
    model = SimpleCTCModel(input_dim=80, hidden_dim=128, output_dim=len(labels))
    text = transcribe('path/to/audio.wav', model, labels)
    print('Transcription:', text)

if __name__ == '__main__':
    main()
