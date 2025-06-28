# Bismillahirrahmanirrahim
# Elhamdulillahi Rabbil Alamin
# Esselatu vesselamu ala Resulina Muhammedin ve ala alihi ve sahbihi ecmain
# Suphanallah, Elhamdulillah, Allahu Ekber
# La ilahe illallah, Muhammedur Resulullah
# La havle ve la kuvvete illa billahil aliyyil azim
# La ilahe illallahu vahdehu la sharika lehu, lehul mulku ve lehul hamdu ve huve ala kulli şey'in kadir


FROM python:3.11-slim

# Gerekli sistem paketlerini yükle
RUN apt-get update && apt-get install -y build-essential ffmpeg && rm -rf /var/lib/apt/lists/*

# Çalışma dizini oluştur
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# FastAPI uygulamasını başlat
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]