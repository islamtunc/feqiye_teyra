# Bismillahir Rahmanir Rahim
# Elhamdu lillahi Rabbil Alamin
# Essalatu was salamu 'ala Rasulillah Wa 'ala alihi wa sahbihi ajma'in
# Allah u Ekber velillahilhamd
# La ilaha illallah, Muhammadur Rasulullah
# SuphanAllah ul Azim, SubhanAllah ul Hamid, SubhanAllah ul Kabir
# Estağfirul El-Azim

import threading
import subprocess
import sys

def run_index():
    # index.py ana dizinde
    subprocess.run([sys.executable, "index.py"])

def run_app():
    # app.py api klasöründe, uvicorn ile başlatılır
    subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_index)
    t2 = threading.Thread(target=run_app)
    t1.start()
    t2.start()
    t1.join()
    t2.join()