"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List

class SimpleCTCModel(nn.Module):
    """
    Simple LSTM-based CTC Model for ASR.
    Args:
        input_dim (int): Feature dimension (e.g., n_mels).
        hidden_dim (int): LSTM hidden size.
        output_dim (int): Number of output classes (vocab size).
        num_layers (int): Number of LSTM layers.
    """
    def __init__(self, input_dim: int, hidden_dim: int, output_dim: int, num_layers: int = 2):
        super(SimpleCTCModel, self).__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers=num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)  # bidirectional

    def forward(self, x: torch.Tensor, x_lens: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [batch, time, feature]
            x_lens: [batch] (lengths of each sequence)
        Returns:
            out: [batch, time, output_dim]
        """
        # Ensure x_lens is on CPU for pack_padded_sequence
        if x_lens.is_cuda:
            x_lens = x_lens.cpu()
        packed = nn.utils.rnn.pack_padded_sequence(x, x_lens, batch_first=True, enforce_sorted=False)
        packed_out, _ = self.lstm(packed)
        out, _ = nn.utils.rnn.pad_packed_sequence(packed_out, batch_first=True)
        out = self.fc(out)
        return out

def ctc_decode(log_probs: torch.Tensor, labels: List[str], blank: int = 0) -> List[str]:
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