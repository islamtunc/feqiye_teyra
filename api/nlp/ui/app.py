"""Bismillahirrahmanirahim
   Elhamdulillahirabbulalemin
   Esselatu vesselamu ala rasulina Muhammedin ve ala alihi ecmain
   ALLAH U Teala bizleri bu ilimden faydalandırsın.
   Amin.
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

class NLPUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('NLP UI - Feqi')
        self.setGeometry(100, 100, 500, 300)
        layout = QVBoxLayout()
        self.label = QLabel('Metni buraya girin:')
        self.textbox = QTextEdit()
        self.result = QLabel('Sonuç:')
        self.button = QPushButton('İşle')
        self.button.clicked.connect(self.process_text)
        layout.addWidget(self.label)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        layout.addWidget(self.result)
        self.setLayout(layout)
    def process_text(self):
        text = self.textbox.toPlainText()
        # Burada NLP işlemi yapılabilir, örnek olarak metni büyük harfe çeviriyoruz
        self.result.setText('Sonuç: ' + text.upper())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NLPUI()
    window.show()
    sys.exit(app.exec_())


