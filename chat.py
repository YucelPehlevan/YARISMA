import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dotenv import load_dotenv
import os
from girisEkrani import *
import degiskenler
import sqlite3
from veritabani import urunleri_veritabanindan_al
from urundeneme import urun_grafik_goster  # Grafik modülünü import et
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1800, 900)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))

        self.kullanici_email = degiskenler.giris_yapan_email
        #self.profil = kullanici_profili_al(self.kullanici_email) 
        self.konusma_gecmisi = []
        self.chat = None
        self.gece_modu = False
        self.urunler = urunleri_veritabanindan_al()  # Liste olarak başlatıldı
        
        try:
            self.kullanici_email = degiskenler.giris_yapan_email
            from veritabani import kullanici_profili_al
            self.profil = kullanici_profili_al(self.kullanici_email)
        except:
            self.kullanici_email = "test@example.com"
            self.profil = {}

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.typeNextChar)
        self.typing_index = 0
        self.typing_text = ""

        self.initUI()

    def initUI(self):
        font = QFont("Arial", 10)

        self.yazi = QLabel("Alışverişle ilgili istediğinizi sorun: ", self)
        self.yazi.setFont(degiskenler.yazi_fontu)
        self.yazi.setGeometry(10, 20, 300, 30)

        self.yazi_kutusu = QTextEdit(self)
        self.yazi_kutusu.setFont(font)
        self.yazi_kutusu.setGeometry(300, 20, 1200, 300)
        self.yazi_kutusu.setPlaceholderText("Bugün ne aramak isterdiniz? ")

        self.urun_yazisi = QLabel("Ürün: ", self)
        self.urun_yazisi.setFont(degiskenler.yazi_fontu)
        self.urun_yazisi.setGeometry(38, 75, 70, 40)

        self.urun_kutusu = QComboBox(self)
        self.urun_kutusu.addItems(degiskenler.urun_listesi)
        self.urun_kutusu.setFont(degiskenler.yazi_fontu)
        self.urun_kutusu.setGeometry(90,70,202,50)
        self.urun_kutusu.currentTextChanged.connect(self.urun_degistir)

        self.butce_yazisi = QLabel("Bütçe: ", self)
        self.butce_yazisi.setFont(degiskenler.yazi_fontu)
        self.butce_yazisi.setGeometry(28, 150, 70, 40)

        self.butce_kutusu = QComboBox(self)
        self.butce_kutusu.addItems(degiskenler.butce_listesi)
        self.butce_kutusu.setFont(degiskenler.yazi_fontu)
        self.butce_kutusu.setGeometry(90,145,202,50)

        self.marka_yazisi = QLabel("Marka: ", self)
        self.marka_yazisi.setFont(degiskenler.yazi_fontu)
        self.marka_yazisi.setGeometry(25, 225, 70, 40)

        self.marka_kutusu = QComboBox(self)
        self.marka_kutusu.addItems(degiskenler.tum_markalar)
        self.marka_kutusu.setFont(degiskenler.yazi_fontu)
        self.marka_kutusu.setGeometry(90,225,202,50)

        self.kullanim_yazisi = QLabel("Kullanım: ", self)
        self.kullanim_yazisi.setFont(degiskenler.yazi_fontu)
        self.kullanim_yazisi.setGeometry(10, 300, 80, 40)

        self.kullanim_kutusu = QComboBox(self)
        self.kullanim_kutusu.addItems(degiskenler.tum_kullanim_amaclari)
        self.kullanim_kutusu.setFont(degiskenler.yazi_fontu)
        self.kullanim_kutusu.setGeometry(90,300,202,50)

        self.mesaj_butonu = QPushButton("Gönder", self)
        self.mesaj_butonu.setGeometry(300, 330, 150, 50)
        self.mesaj_butonu.setFont(degiskenler.buton_fontu)
        self.mesaj_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.mesaj_butonu.clicked.connect(self.sendMessage)

        # YENİ: Grafik göster butonu
        self.grafik_butonu = QPushButton("📊 Grafik Göster", self)
        self.grafik_butonu.setGeometry(470, 330, 300, 50)
        self.grafik_butonu.setFont(degiskenler.buton_fontu)
        self.grafik_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.grafik_butonu.clicked.connect(self.grafik_goster)
        self.grafik_butonu.setEnabled(False)  # Başlangıçta deaktif

        self.oneri_butonu = QPushButton("Önerileri Göster", self)
        self.oneri_butonu.setGeometry(50, 610, 200, 70)
        self.oneri_butonu.setFont(degiskenler.buton_fontu)
        self.oneri_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.oneri_butonu.clicked.connect(self.onceki_onerileri_goster)

        self.cikis_butonu = QPushButton("Çıkış Yap", self)
        self.cikis_butonu.setGeometry(50, 780, 200, 70)
        self.cikis_butonu.setFont(degiskenler.buton_fontu)
        self.cikis_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.cikis_butonu.clicked.connect(self.cikis_yap)

        self.mod_butonu = QPushButton("🌙 Gece Modu",self)
        self.mod_butonu.setGeometry(1550,10,200,100)
        self.mod_butonu.setFont(degiskenler.buton_fontu)
        self.mod_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.mod_butonu.clicked.connect(self.mod_degistir)

        self.temizleme_butonu = QPushButton("Sohbeti Sil", self)
        self.temizleme_butonu.setGeometry(50,695,200,70)
        self.temizleme_butonu.setFont(degiskenler.buton_fontu)
        self.temizleme_butonu.setStyleSheet("""
            QPushButton {
                background-color: #000000;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        self.temizleme_butonu.clicked.connect(self.sohbet_gecmisini_temizle) 

        self.sonuc_kutusu = QTextEdit(self)
        # Gece modu için CSS ayarı
        if self.gece_modu:
            self.sonuc_kutusu.setStyleSheet("QTextEdit { background-color: #2b2b2b; color: white; }")
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.setFont(font)
        self.sonuc_kutusu.setGeometry(300, 400, 1200, 450)
        self.sonuc_kutusu.append("Asistan: Merhaba! Alışveriş asistanına hoş geldiniz.")
        self.sonuc_kutusu.append("Asistan: Nasıl yardımcı olabilirim?")
        #self.gecmisi_yukle()

    def sendMessage(self):
        kullanici_girdisi = self.yazi_kutusu.toPlainText().strip()
        if not kullanici_girdisi:
            return
        """
        self.konusma_gecmisi.append(f"<b><span style='color:#007bff;'>Siz:</span></b> {kullanici_girdisi}")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        self.yazi_kutusu.clear()

        self.konusma_gecmisi.append(f"<b><span style='color:#6c757d;'>Asistan:</span></b> Yanıtınız hazırlanıyor...")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        QApplication.processEvents()
        """
        # Gemini API - dosyanın başına import ekleyin
        if not hasattr(self, 'model'):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("models/gemini-2.0-flash")
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Gemini API hatası: {str(e)}")
                return

        # Ürün verilerini listeye göre formatla
        urun_verisi = ""
        for urun in self.urunler:
            # urun tuple'ı: (urun_turu, marka, model, fiyat)
            urun_turu, marka, model, fiyat = urun
            urun_verisi += f"{urun_turu} - Marka: {marka}, Model: {model}, Fiyat: {fiyat}\n"

        prompt = f"""
        Sen uzman bir alışveriş danışmanısın. Kullanıcıya kişiselleştirilmiş ürün önerileri sunacaksın.

        📋 GÖREV:
        - Kullanıcının ihtiyaçlarını analiz et
        - En uygun 2-3 ürün öner (fazla seçenek verme)
        - Her önerinin nedenini açıkla
        - Fiyat-performans değerlendirmesi yap

        🛍️ MEVCUT ÜRÜNLER:
        {urun_verisi}

        👤 KULLANICI PROFİLİ:
        - Cinsiyet: {self.profil.get('cinsiyet', 'Belirtilmemiş')}
        - Yaş: {self.profil.get('yas', 'Belirtilmemiş')}
        - Meslek: {self.profil.get('meslek', 'Belirtilmemiş')}
        - Eğitim: {self.profil.get('egitim', 'Belirtilmemiş')}
        - Fiziksel Özellikler: Boy {self.profil.get('boy', 'Belirtilmemiş')}, Kilo {self.profil.get('kilo', 'Belirtilmemiş')}

        🎯 KULLANICI TALEPLERİ:
        - Aranan Ürün: {self.urun_kutusu.currentText()}
        - Kullanım Amacı: {self.kullanim_kutusu.currentText()}
        - Bütçe: {self.butce_kutusu.currentText()}
        - Marka Tercihi: {self.marka_kutusu.currentText()}

        💬 KULLANICI MESAJI: "{kullanici_girdisi}"

        📝 CEVAP FORMATI:
        1. Kısa selamlama ve ihtiyaç özetı
        2. En uygun 2-3 ürün önerisi (her biri için):
           - Ürün adı ve fiyatı
           - Neden bu ürün? (kişisel özelliklerine uygunluk)
           - Artı/eksi yönleri
        3. Final önerisi ve nedeni
        4. Ek sorular (gerekirse)
        

        ⚡ KURALLAR:
        - Samimi ve profesyonel ol
        - Sadece mevcut ürünlerden öner
        - Bütçe '-' ise bütçe sor
        - Marka 'Farketmez' ise marka sorma
        - Çok detaya girme, net ol
        - Emojiler kullan ama abartma
        - Eğer kulanıcı bir ürünü almaya karar verirse kısa ve samimi bir dille doğru kararı verdiği söyle
        """

        if self.chat is None:
            self.chat = self.model.start_chat(history=[])
        
        cevap = self.chat.send_message(prompt)
        self.sohbeti_kaydet(kullanici_girdisi, cevap.text)

        # Kullanıcı mesajı hemen gösterilir
        self.konusma_gecmisi.append(f"<b><span style='color:black;'>Siz:</span></b> {kullanici_girdisi}")
        self.konusma_gecmisi.append(f"<b><span style='color:blue;'>Asistan:</span></b> ")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))

        # Typing efekt verisi
        formatli_cevap = self.ai_cevabini_formatla(cevap.text)
        self.typing_text = formatli_cevap

        self.typing_index = 0
        self.typing_timer.start(15)

    def urun_degistir(self,secilen_urun):
        self.marka_kutusu.clear()
        self.kullanim_kutusu.clear()

        self.marka_kutusu.addItems(degiskenler.marka_listeleri.get(secilen_urun,[]))
        self.kullanim_kutusu.addItems(degiskenler.kullanim_amaci_listeleri.get(secilen_urun,[]))

    def sohbeti_kaydet(self, kullanici_girdi, asistan_cevabi):
        dosya_adi = f"gecmisler/{degiskenler.giris_yapan_email}.txt"
        os.makedirs("gecmisler", exist_ok=True)
        with open(dosya_adi, "a", encoding="utf-8") as f:
            f.write(f"Kullanıcı: {kullanici_girdi}\n")
            f.write(f"Asistan: {asistan_cevabi}\n\n")

    def grafik_goster(self):
        """Önerilen ürünler için grafik pencerelerini aç"""
        if not self.son_onerilen_urunler:
            QMessageBox.information(self, "Bilgi", "Önce bir ürün önerisi alın!")
            return
        
        try:
            # Her önerilen ürün için grafik penceresi aç
            for urun_adi in self.son_onerilen_urunler:
                grafik_penceresi = urun_grafik_goster(urun_adi, self)
                self.grafik_pencereleri.append(grafik_penceresi)
            
            # Başarı mesajı
            QMessageBox.information(self, "Başarılı", 
                                  f"{len(self.son_onerilen_urunler)} ürün için grafik pencereleri açıldı!")
            
        except ImportError:
            QMessageBox.warning(self, "Hata", 
                              "Grafik modülü yüklenemiyor! matplotlib yüklü olduğundan emin olun.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Grafik gösterilirken hata oluştu: {str(e)}")        

    def ai_cevabini_formatla(self, metin):
        """AI'dan gelen metni HTML formatına çevirir"""
        
        # Başlık olacak kalıpları tanımla
        baslik_kaliplari = [
            "**Öneriler:**",
            "**Neden bu ürün?**", 
            "**Artıları:**",
            "**Eksileri:**",
            "**Final Önerisi:**",
            "**Avantajları:**",
            "**Dezavantajları:**"
        ]
        
        # Her başlık kalıbını HTML başlığına çevir - CSS class kullan
        for kalip in baslik_kaliplari:
            temiz_baslik = kalip.replace("**", "").replace("*", "")
            # CSS class ile - inline style yerine
            html_baslik = f"<h3 class='baslik-stili'>{temiz_baslik}</h3>"
            metin = metin.replace(kalip, f"<br>{html_baslik}")
        
        # Ürün isimlerini ayrı satıra al
        import re
        metin = re.sub(r'(\d+\.)\s+([A-Za-zÇĞIİÖŞÜçğıiöşü\s\d\-]+(?:\([^)]*\))?)', r'<br><b>\1 \2</b>', metin)
        
        # Diğer ** kalın yazıları normal HTML bold'a çevir
        metin = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', metin)
        metin = re.sub(r'\*\*\*(.*?)\*\*', r'<b>\1</b>', metin)
        
        return metin  

    def gecmisi_yukle(self):
        dosya_adi = f"gecmisler/{degiskenler.giris_yapan_email}.txt"
        if os.path.exists(dosya_adi):
            with open(dosya_adi, "r", encoding="utf-8") as f:
                gecmis = f.read()
                gecmis_html = "<br>".join(gecmis.splitlines())
                self.konusma_gecmisi.append(gecmis_html)
                self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))

    def sohbet_gecmisini_temizle(self):
        self.konusma_gecmisi.clear()
        self.sonuc_kutusu.clear()

    def onceki_onerileri_goster(self):
        import os

        email = degiskenler.giris_yapan_email
        dosya_yolu = f"gecmisler/{email}.txt"
        self.sonuc_kutusu.clear()
        if not os.path.exists(dosya_yolu):
            self.sonuc_kutusu.append("Daha önceki önerilere ulaşılamadı.")
            return

        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()

        oneriler = []
        for i, satir in enumerate(satirlar):
            if satir.startswith("1.") or satir.startswith("2.") or satir.startswith("3.") or satir.startswith("**1.") or satir.startswith("**2.") or satir.startswith("**3."):
                oneriler.append(satirlar[i].strip())  # Asıl ürün listesi bir sonraki satırda olabilir

        if oneriler:
            mesaj = "İşte önceki bazı ürün önerilerin:\n\n" + "\n".join(f"• {o}" for o in oneriler[:])  # Son 5 tanesi
        else:
            mesaj = "Daha önce sana özel bir ürün önerisi sunulmamış."
        self.sonuc_kutusu.append(mesaj)
    

    def mod_degistir(self):
        mevcut_html = self.sonuc_kutusu.toHtml()
        if not self.gece_modu:
            self.gece_modu = True
            self.mod_butonu.setText("☀️ Gündüz Modu")

            self.sonuc_kutusu.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: white;
            }
            .baslik-stili {
                color: white !important;
                font-size: 16px;
                font-weight: bold;
            }
            """)

            # Gece modu renkleri
            palet = QPalette()
            palet.setColor(QPalette.Window, QColor(53, 53, 53))
            palet.setColor(QPalette.WindowText, Qt.white)
            palet.setColor(QPalette.Base, QColor(35, 35, 35))
            palet.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palet.setColor(QPalette.ToolTipBase, Qt.white)
            palet.setColor(QPalette.ToolTipText, Qt.white)
            palet.setColor(QPalette.Text, Qt.white)
            palet.setColor(QPalette.Button, QColor(53, 53, 53))
            palet.setColor(QPalette.ButtonText, Qt.white)
            palet.setColor(QPalette.BrightText, Qt.red)
            palet.setColor(QPalette.Link, QColor(42, 130, 218))
            palet.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palet.setColor(QPalette.HighlightedText, Qt.black)
            mevcut_html = mevcut_html.replace("color: black;", "color: white;")
            QApplication.setPalette(palet)                              

        else:
            self.gece_modu = False
            self.mod_butonu.setText("🌙 Gece Modu")

            self.sonuc_kutusu.setStyleSheet("""
            QTextEdit {
                background-color: white;
                color: black;
            }
            .baslik-stili {
                color: black !important;
                font-size: 16px;
                font-weight: bold;
            }
            """)                                
            mevcut_html = mevcut_html.replace("color: white;", "color: black;")
            QApplication.setPalette(QApplication.style().standardPalette())

        self.sonuc_kutusu.setHtml(mevcut_html)    
           
    def typeNextChar(self):
        if self.typing_index < len(self.typing_text):
            metin = self.typing_text[:self.typing_index + 1]
            full_html = "<br><br>".join(self.konusma_gecmisi[:-1]) + f"<br><br><b><span style='color:blue;'>Asistan:</span></b> {metin}"
            self.sonuc_kutusu.setHtml(full_html)
            self.typing_index += 1
        else:
            self.konusma_gecmisi[-1] += self.typing_text
            self.typing_timer.stop()

    def cikis_yap(self):
        from girisEkrani import LoginRegisterWindow
        cevap = QMessageBox.question(self, "Çıkış Yap", "Giriş ekranına dönmek istiyor musunuz?",
                                  QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.login_window = LoginRegisterWindow()
            self.login_window.show()
            self.hide()  # veya self.hide()       

def main():
    app = QApplication(sys.argv)
    app.setPalette(QApplication.style().standardPalette())
    giris_ekrani = ChatWindow()
    giris_ekrani.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()