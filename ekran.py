import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dotenv import load_dotenv
import os

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

# Basit ürün veri seti
urunler = {
    "Samsung Galaxy S23": {
        "fiyat": "35.000 TL",
        "özellikler": "8 GB RAM, 128 GB hafıza, 50 MP kamera, 3900 mAh batarya"
    },
    "iPhone 14": {
        "fiyat": "47.000 TL",
        "özellikler": "6 GB RAM, 128 GB hafıza, 12 MP kamera, 3279 mAh batarya"
    },
    "Xiaomi Redmi Note 12": {
        "fiyat": "10.500 TL",
        "özellikler": "6 GB RAM, 128 GB hafıza, 50 MP kamera, 5000 mAh batarya"
    },
    "Realme C55": {
        "fiyat": "8.200 TL",
        "özellikler": "8 GB RAM, 256 GB hafıza, 64 MP kamera, 5000 mAh batarya"
    },
    "POCO X5 Pro": {
        "fiyat": "13.500 TL",
        "özellikler": "8 GB RAM, 256 GB hafıza, 108 MP kamera, Snapdragon 778G"
    },
    "Vestel Venus E5": {
        "fiyat": "4.900 TL",
        "özellikler": "3 GB RAM, 32 GB hafıza, 13 MP kamera, 4000 mAh batarya"
    },
    "Samsung Galaxy A34": {
        "fiyat": "14.500 TL",
        "özellikler": "6 GB RAM, 128 GB hafıza, 48 MP kamera, 5000 mAh batarya"
    },
    "iPhone SE (3. Nesil)": {
        "fiyat": "26.000 TL",
        "özellikler": "4 GB RAM, 64 GB hafıza, 12 MP kamera, A15 Bionic işlemci"
    },
    "Huawei Nova 9": {
        "fiyat": "15.000 TL",
        "özellikler": "8 GB RAM, 128 GB hafıza, 50 MP kamera, 66W hızlı şarj"
    },
    "General Mobile GM 24 Pro": {
        "fiyat": "7.200 TL",
        "özellikler": "8 GB RAM, 256 GB hafıza, 108 MP kamera, 5000 mAh batarya"
    }
}

load_dotenv()
api_key = os.getenv("API_KEY")

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))

        self.konusma_gecmisi = []
        self.chat = None
        self.urunler = urunler

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.typeNextChar)
        self.typing_index = 0
        self.typing_text = ""

        self.initUI()

    def initUI(self):
        font = QFont("Arial", 10)

        self.yazi = QLabel("Alışverişle ilgili istediğinizi sorun: ", self)
        self.yazi.setFont(font)
        self.yazi.setGeometry(10, 20, 300, 20)

        self.yazi_kutusu = QTextEdit(self)
        self.yazi_kutusu.setFont(font)
        self.yazi_kutusu.setGeometry(250, 20, 1100, 300)

        self.buton = QPushButton("Gönder", self)
        self.buton.setGeometry(250, 330, 100, 30)
        self.buton.clicked.connect(self.sendMessage)

        self.sonuc_kutusu = QTextEdit(self)
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.setFont(font)
        self.sonuc_kutusu.setGeometry(250, 400, 1100, 450)

    def sendMessage(self):
        kullanici_girdisi = self.yazi_kutusu.toPlainText().strip()
        if not kullanici_girdisi:
            return

        # Gemini API
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        urun_verisi = ""
        for urun, detay in self.urunler.items():
            urun_verisi += f"{urun} - Fiyat: {detay['fiyat']}, Özellikler: {detay['özellikler']}\n"

        prompt = f"""
        Sen bir alışveriş asistanısın. Aşağıdaki ürünleri incele ve sadece kullanıcının ihtiyaçlarına uygun olanları öner. 
        Kullanıcının ihtiyacını analiz et ve buna göre ürünleri filtrele. Hafızanı kullanarak önceki mesajları hatırla.

        Ürün Listesi:
        {urun_verisi}

        Kullanıcının mesajı:
        "{kullanici_girdisi}"

        Cevabını sadece uygun ürünleri önererek ver. Gerekirse önce sorular sorabilirsin (örneğin bütçesi nedir, hangi marka vs.).
        """

        if self.chat is None:
            self.chat = model.start_chat(history=[])
        cevap = self.chat.send_message(prompt)

        # Kullanıcı mesajı hemen gösterilir
        self.konusma_gecmisi.append(f"<b><span style='color:black;'>Kullanıcı:</span></b> {kullanici_girdisi}")
        self.konusma_gecmisi.append(f"<b><span style='color:blue;'>Asistan:</span></b> ")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))

        # Typing efekt verisi
        self.typing_text = cevap.text
        self.typing_index = 0
        self.typing_timer.start(15)

        self.yazi_kutusu.clear()

    def typeNextChar(self):
        if self.typing_index < len(self.typing_text):
            metin = self.typing_text[:self.typing_index + 1]
            full_html = "<br><br>".join(self.konusma_gecmisi[:-1]) + f"<br><br><b><span style='color:blue;'>Asistan:</span></b> {metin}"
            self.sonuc_kutusu.setHtml(full_html)
            self.typing_index += 1
        else:
            self.konusma_gecmisi[-1] += self.typing_text
            self.typing_timer.stop()


def main():
    app = QApplication(sys.argv)
    pencere = Window()
    pencere.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
