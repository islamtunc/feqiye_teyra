#Bismillahirrahmanirahim
#Elhamdulillahirabbulalemin
# Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ve sahbihi ecmain
# Allah u Ekber velillahilhamd
# La ilahe illallah Muhammedur Rasulullah
# SuphanAllahilazim ve bihamdihi
# La havle ve la kuvvete illa billahil aliyyil azim
# Hasbunallahu ve ni'mel vekil

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

import torch
import sys
import os

# Model ve tokenizer'ı bir kez yükle
from api.nlp.llm import SimpleCharTransformerLM
from api.nlp.tokenizer import SimpleTokenizer

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../nlp/llm_model.pth')
MODEL_PATH = os.path.abspath(MODEL_PATH)

# Model ve tokenizer yükle
if os.path.exists(MODEL_PATH):
    checkpoint = torch.load(MODEL_PATH, map_location='cpu')
    vocab = checkpoint['vocab']
    tokenizer = SimpleTokenizer()
    tokenizer.vocab = vocab
    vocab_size = len(tokenizer.vocab)
    model = SimpleCharTransformerLM(vocab_size=vocab_size)
    model.load_state_dict(checkpoint['model'])
    model.eval()
else:
    model = None
    tokenizer = None

router = APIRouter()

def generate_reply(prompt, max_new_tokens=50):
    if model is None or tokenizer is None:
        return "AI hazır değil."
    input_ids = tokenizer.encode(prompt)
    x = torch.tensor([input_ids], dtype=torch.long)
    for _ in range(max_new_tokens):
        with torch.no_grad():
            logits = model(x)
            next_token_logits = logits[0, -1]
            next_token = torch.argmax(next_token_logits).item()
        x = torch.cat([x, torch.tensor([[next_token]])], dim=1)
        if tokenizer.decode([next_token]) in ['\n', '.', '!', '?']:
            break
    output = tokenizer.decode(x[0].tolist())
    return output[len(prompt):].strip() or "..."

@router.post("/")
async def chat_endpoint(request: Request):
    data = await request.json()
    message = data.get("message", "")
    # LLM ile cevap üret
    reply = generate_reply(message)
    return JSONResponse(content={"reply": reply})
