#Bismillahirrahmanirahim
#Elhamdulillahirabbulalemin
#SuphanAllah ul Azim ve Bihamdihi
#Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ve sahbihi ecmain.
#Allahu Ekber velillahilhamd
#La ilahe illallâhü vahdehu la şerike leh, lehul mulku lehul hamdu.


# url_to_txt.py

import requests
from bs4 import BeautifulSoup
import re

def urlden_txt_olustur(url, dosya_adi="metin.txt", min_uzunluk=30):
    try:
        print(f"[+] URL işleniyor: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Bağlantı hatası varsa hata ver
        soup = BeautifulSoup(response.content, "html.parser")

        # Paragrafları çek ve temizle
        paragraflar = [
            p.get_text(strip=True)
            for p in soup.find_all("p")
            if len(p.get_text(strip=True)) > min_uzunluk
        ]

        if not paragraflar:
            print("[-] Uygun uzunlukta paragraf bulunamadı.")
            return

        metin = "\n\n".join(paragraflar)

        # Basit temizlik
        metin = re.sub(r"\s+", " ", metin)      # fazla boşluklar
        metin = re.sub(r"\[\d+\]", "", metin)   # [1], [2] gibi kaynak referansları
        metin = metin.strip()

        # Dosyaya kaydet
        with open(dosya_adi, "w", encoding="utf-8") as f:
            f.write(metin)

        print(f"[✓] Metin başarıyla kaydedildi: {dosya_adi}")

    except Exception as e:
        print(f"[!] Hata oluştu: {e}")


# ---------- Örnek kullanım ----------
if __name__ == "__main__":
    url = "https://tr.wikipedia.org/wiki/Yapay_zeka"  # buraya URL'yi gir
    urlden_txt_olustur(url, dosya_adi="yapay_zeka.txt")
