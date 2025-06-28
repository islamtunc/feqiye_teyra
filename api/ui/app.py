"""
Basit bir PyQt5 tabanlı kullanıcı arayüzü iskeleti.
Bu arayüz, ASR, TTS ve NLP modüllerinizle entegre edilebilir.
"""
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ASR & TTS & NLP Demo')
        self.layout = QVBoxLayout()
        self.textbox = QTextEdit()
        self.result = QLabel('Sonuç:')
        self.open_btn = QPushButton('Ses Dosyası Aç')
        self.transcribe_btn = QPushButton('Sesi Yazıya Çevir')
        self.tts_btn = QPushButton('Metni Sese Çevir')
        self.layout.addWidget(self.open_btn)
        self.layout.addWidget(self.transcribe_btn)
        self.layout.addWidget(self.tts_btn)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.result)
        self.setLayout(self.layout)
        self.open_btn.clicked.connect(self.open_file)
        # self.transcribe_btn.clicked.connect(self.transcribe_audio)
        # self.tts_btn.clicked.connect(self.text_to_speech)
        self.audio_path = None
    def open_file(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Ses Dosyası Seç', '', 'WAV Files (*.wav)')
        if fname:
            self.audio_path = fname
            self.result.setText(f'Seçilen dosya: {fname}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
