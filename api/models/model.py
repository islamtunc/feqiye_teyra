"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""

# ASR Model with CTC Loss and Greedy Decoding



import torch
import torchaudio
import torch.nn as nn
import torch.nn.functional as F

class SimpleCTCModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers=2):
        super(SimpleCTCModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)  # bidirectional
    def forward(self, x, x_lens):
        packed = nn.utils.rnn.pack_padded_sequence(x, x_lens, batch_first=True, enforce_sorted=False)
        packed_out, _ = self.lstm(packed)
        out, _ = nn.utils.rnn.pad_packed_sequence(packed_out, batch_first=True)
        out = self.fc(out)
        return out

def ctc_decode(log_probs, labels, blank=0):
    """
    Greedy CTC decoding.
    Args:
        log_probs (Tensor): [batch, time, classes] (log softmax output)
        labels (list): List of label tokens (e.g. ['a','b','c',' '])
        blank (int): Index of blank token
    Returns:
        List of decoded strings
    """
    pred = torch.argmax(log_probs, dim=-1)
    results = []
    for seq in pred:
        prev = blank
        out = []
        for idx in seq:
            idx = idx.item()
            if idx != prev and idx != blank:
                out.append(labels[idx])
            prev = idx
        results.append(''.join(out))
    return results