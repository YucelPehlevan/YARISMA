import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dotenv import load_dotenv
import os
from PyQt5.QtWidgets import QWidget
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

load_dotenv()
api_key = os.getenv("API_KEY")

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200,200,800,800)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))
        self.konusma_gecmisi = []
        self.chat = None
        self.initUI()

    def initUI(self):
        self.yazi = QLabel(self)
        self.yazi.move(20,20)
        self.yazi.resize(200,20)
        self.yazi.setText("Alışverişle ilgili istediğinizi sorun: ")

        self.yazi_kutusu = QTextEdit(self)
        self.yazi_kutusu.move(220,20)
        self.yazi_kutusu.resize(500,150)

        self.buton = QPushButton(self)
        self.buton.move(270,180)
        self.buton.setText("gönder")
        self.buton.clicked.connect(self.sendMessage)

        self.sonuc_kutusu = QTextEdit(self)
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.move(220, 250)
        self.sonuc_kutusu.resize(500, 400)

    def sendMessage(self):
        kullanici_girdisi = self.yazi_kutusu.toPlainText()

        # Gemini API çağrısı
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        if self.chat==None:
            self.chat = model.start_chat()
            cevap = self.chat.send_message(kullanici_girdisi)
        else:
            cevap = self.chat.send_message(kullanici_girdisi)    

        # Yanıtı kullanıcıya göster (örnek olarak popup)
        self.konusma_gecmisi.append(f"<b><span style='color:black;'>Kullanıcı:</span></b> {kullanici_girdisi}")
        self.konusma_gecmisi.append(f"<b><span style='color:blue;'>Asistan:</span></b> {cevap.text}")

        # Arayüz güncelleme
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        self.yazi_kutusu.clear()

def main():
    uygulama = QApplication(sys.argv)
    ekran = Window()

    ekran.show()
    sys.exit(uygulama.exec_())  

if __name__ == "__main__":
    main()          

