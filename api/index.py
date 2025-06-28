# Bismillahir Rahmanir Rahim
# Elhamdu lillahi Rabbil Alamin
# Essalatu was salamu 'ala Rasulillah Wa 'ala alihi wa sahbihi ajma'in
# Allah u Ekber velillahilhamd
# La ilaha illallah, Muhammadur Rasulullah
# SuphanAllah ul Azim, SubhanAllah ul Hamid, SubhanAllah ul Kabir
# Estağfirul El-Azim


from http.server import BaseHTTPRequestHandler

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
            <title>AI Asistan</title>
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
            </style>
        </head>
        <body>
            <div class="container">
                <div class="ai-icon">🤖</div>
                <h1>AI Asistan</h1>
                <p>Merhaba! Ben sizin akıllı asistanınızım.<br>Her türlü sorunuz için buradayım.</p>
                <div class="footer">© 2025 AI Asistan Projesi</div>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
        return
