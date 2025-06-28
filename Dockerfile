# Bismillahirrahmanirrahim
# Elhamdulillahi Rabbil Alamin
# Esselatu vesselamu ala Resulina Muhammedin ve ala alihi ve sahbihi ecmain
# Suphanallah, Elhamdulillah, Allahu Ekber
# La ilahe illallah, Muhammedur Resulullah
# La havle ve la kuvvete illa billahil aliyyil azim
# La ilahe illallahu vahdehu la sharika lehu, lehul mulku ve lehul hamdu ve huve ala kulli şey'in kadir


FROM python:3.11-slim

# Gerekli sistem paketlerini yükle ve temizle
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential ffmpeg \
    && apt-get purge -y --auto-remove build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip cache purge

# Sadece gerekli dosyaları kopyala (örnek: .py dosyaları ve data/model klasörleri)
COPY api/ ./api/
COPY models/ ./models/
COPY requirements.txt .
COPY vercel.json .
COPY README.md .
COPY . .

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]