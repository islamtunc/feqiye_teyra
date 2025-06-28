"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""
"""
NLP (Doğal Dil İşleme) Modülleri için temel mimari.
Bu klasör, ASR ve TTS projelerinizle uyumlu şekilde metin işleme, tokenizasyon, dil modeli vb. için kullanılabilir.
"""
import re

class SimpleTokenizer:
    def __init__(self, vocab=None):
        self.vocab = vocab or {}
        self.inv_vocab = {v: k for k, v in self.vocab.items()}
    def fit(self, texts):
        chars = set(''.join(texts))
        self.vocab = {c: i for i, c in enumerate(sorted(chars))}
        self.inv_vocab = {i: c for c, i in self.vocab.items()}
    def encode(self, text):
        return [self.vocab.get(c, 0) for c in text]
    def decode(self, ids):
        return ''.join([self.inv_vocab.get(i, '') for i in ids])

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zçğıöşü\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Kullanım örneği:
# tokenizer = SimpleTokenizer()
# tokenizer.fit(["örnek metin", "başka bir cümle"])
# ids = tokenizer.encode("örnek metin")
# text = tokenizer.decode(ids)
