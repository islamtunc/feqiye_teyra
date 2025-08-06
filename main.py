# Bismillahir Rahmanir Rahim
# Elhamdu lillahi Rabbil Alamin
# Essalatu was salamu 'ala Rasulillah Wa 'ala alihi wa sahbihi ajma'in
# Allah u Ekber velillahilhamd
# La ilaha illallah, Muhammadur Rasulullah
# SuphanAllah ul Azim, SubhanAllah ul Hamid, SubhanAllah ul Kabir
# Estağfirullah El-Azim
# Allahumma salli 'ala Muhammad wa 'ala ali Muhammad
# Elhamdu lillahi Rabbil Alamin
import threading
import subprocess
import sys

from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = """
        <!DOCTYPE html>
        <html lang="tr">
        <head>
            <meta charset="UTF-8">
            <title>Feqîyê Teyran</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {
                    background: linear-gradient(135deg, #4f8cff 0%, #a6ffcb 100%);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .container {
                    background: rgba(255,255,255,0.95);
                    border-radius: 18px;
                    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
                    padding: 40px 32px;
                    max-width: 400px;
                    text-align: center;
                }
                h1 {
                    color: #2d3a4b;
                    margin-bottom: 12px;
                }
                p {
                    color: #4f8cff;
                    font-size: 1.1em;
                    margin-bottom: 24px;
                }
                .ai-icon {
                    font-size: 48px;
                    margin-bottom: 16px;
                    color: #4f8cff;
                }
                .footer {
                    margin-top: 24px;
                    font-size: 0.9em;
                    color: #888;
                }
                .message-box {
                    display: flex;
                    margin-top: 20px;
                }
                .message-input {
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #b3c6ff;
                    border-radius: 8px 0 0 8px;
                    font-size: 1em;
                    outline: none;
                }
                .send-btn {
                    padding: 10px 18px;
                    background: #4f8cff;
                    color: #fff;
                    border: none;
                    border-radius: 0 8px 8px 0;
                    font-size: 1em;
                    cursor: pointer;
                    transition: background 0.2s;
                }
                .send-btn:hover {
                    background: #357ae8;
                }
                .reply-area {
                    margin-top: 18px;
                    color: #2d3a4b;
                    min-height: 24px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="ai-icon">🤖</div>
                <h1>Feqîyê Teyran</h1>
                <p>Selam Aleykum ez Feqi fermo.....<br>Kurdish AI Asisstant</p>
                <form class="message-box" id="msgForm">
                    <input class="message-input" id="msgInput" type="text" placeholder="Dest bi axaftinê bikin.." required />
                    <button class="send-btn" type="button" id="recordBtn">🎤 Deng </button>
                </form>
                <audio id="audioPlayback" controls style="display:none;"></audio>
                <div class="reply-area" id="replyArea"></div>
                <div class="footer">© 2025 Yekazad</div>
            </div>
            <script>
                document.getElementById('msgForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    const input = document.getElementById('msgInput');
                    const replyArea = document.getElementById('replyArea');
                    const message = input.value;
                    replyArea.textContent = "Gönderiliyor...";
                    try {
                        const res = await fetch('/api/chat/', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({message})
                        });
                        const data = await res.json();
                        replyArea.textContent = data.reply;
                    } catch (err) {
                        replyArea.textContent = "Bir hata oluştu.";
                    }
                    input.value = "";
                });

let mediaRecorder;
let audioChunks = [];
let audioBlob = null;

const recordBtn = document.getElementById('recordBtn');
const sendAudioBtn = document.getElementById('sendAudioBtn');
const audioPlayback = document.getElementById('audioPlayback');

recordBtn.addEventListener('click', async function() {
    if (mediaRecorder && mediaRecorder.state === "recording") {
        mediaRecorder.stop();
        recordBtn.textContent = "🎤 Ses Kaydet";
    } else {
        if (navigator.mediaDevices) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            mediaRecorder.ondataavailable = e => audioChunks.push(e.data);
            mediaRecorder.onstop = () => {
                audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                audioPlayback.src = URL.createObjectURL(audioBlob);
                audioPlayback.style.display = "block";
                sendAudioBtn.disabled = false; // Gönder butonunu aktif et
            };
            mediaRecorder.start();
            recordBtn.textContent = "Durdur";
            sendAudioBtn.disabled = true; // Kayıt sırasında gönderme kapalı
        }
    }
});

sendAudioBtn.addEventListener('click', async function() {
    if (!audioBlob) return;
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.wav');
    const res = await fetch('/asr/', {
        method: 'POST',
        body: formData
    });
    const data = await res.json();
    document.getElementById('replyArea').textContent = data.transcript || "Ses çözümlenemedi.";
    sendAudioBtn.disabled = true; // Gönderildikten sonra tekrar pasif yap
});
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        return

    def do_POST(self):
        if self.path in ["/api/message/", "/api/chat/"]:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            import json
            data = json.loads(body)
            message = data.get("message", "")
            reply = f"Pirsa we: {message}"
            response = {"reply": reply}
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def run_http_server():
    port = int(os.environ.get("PORT", 8000))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, handler)
    print(f"Serving on http://0.0.0.0:{port}")
    httpd.serve_forever()

def run_app():
    # app.py api klasöründe, uvicorn ile başlatılır
    subprocess.run([sys.executable, "-m", "uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8001"])

if __name__ == "__main__":
    t1 = threading.Thread(target=run_http_server)
    t2 = threading.Thread(target=run_app)
    t1.start()
    t2.start()
    t1.join()
    t2.join()