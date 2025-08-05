import sys
import os
import degiskenler
from dotenv import load_dotenv
from classes import *

load_dotenv()

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle("Alışveriş Asistanı - Premium Edition")
        self.setWindowIcon(QIcon("robot.png")) #<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Hilmy Abiyyu A. - Flaticon</a>
        self.gece_modu = True
        
        # modern gorunum için ayarlamalar
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.initUI()
        self.animasyonu_hazirla()

    def initUI(self):
        self.ana_govde = QWidget(self)
        self.setCentralWidget(self.ana_govde)
        
        # animasyonlu arka plan
        self.arkaplan = AnimatedBackground(self)
        self.arkaplan.setGeometry(0, 0, 1600, 900)
        
        # parlama efektli başlık
        self.baslik_yazisi = QLabel("✨ Alışveriş Asistanı ✨", self)
        self.baslik_yazisi.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.baslik_yazisi.setAlignment(Qt.AlignCenter)
        self.baslik_yazisi.setGeometry(200, 50, 1200, 80)
        self.baslik_yazisi.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            }
        """)
        
        # altyazi
        self.altyazi = QLabel("Premium alışveriş deneyimi için giriş yapın", self)
        self.altyazi.setFont(QFont("Segoe UI", 16))
        self.altyazi.setAlignment(Qt.AlignCenter)
        self.altyazi.setGeometry(200, 130, 1200, 40)
        self.altyazi.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
        """)
        
        # Ekran kontrolü
        self.ekran_kontrolunu_baslat()
        
        # Giriş ve Kayıt kartları
        self.giris_kartini_baslat()
        self.kayit_kartini_baslat()
        
        # Mode değiştirme butonunu başlat
        self.mode_butonunu_baslat()

    def ekran_kontrolunu_baslat(self):
        #  çıkış butonu ayarları
        self.cikis_butonu = QPushButton("✕", self)
        self.cikis_butonu.setGeometry(1540, 20, 40, 40)
        self.cikis_butonu.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 0, 0, 0.8);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 0, 0, 1);
                transform: scale(1.1);
            }
        """)
        self.cikis_butonu.clicked.connect(self.uygulamayi_kapat)
        
        # küçültme butonu ayarları
        self.kucultme_butonu = QPushButton("—", self)
        self.kucultme_butonu.setGeometry(1490, 20, 40, 40)
        self.kucultme_butonu.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 193, 7, 0.8);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 193, 7, 1);
            }
        """)
        self.kucultme_butonu.clicked.connect(self.showMinimized)

    def giris_kartini_baslat(self):
        # Giriş kartı
        self.giris_karti = FloatingCard(self)
        self.giris_karti.setGeometry(200, 250, 450, 500)
        self.giris_karti.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Giriş Yap yazısı
        giris_basligi = QLabel("🔐 Giriş Yap", self.giris_karti)
        giris_basligi.setFont(QFont("Segoe UI", 24, QFont.Bold))
        giris_basligi.setAlignment(Qt.AlignCenter)
        giris_basligi.setGeometry(50, 30, 350, 50)
        giris_basligi.setStyleSheet("color: white; background: transparent; border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3);")
        
        # Email Alanı
        self.email_yazisi = QLabel("📧 E-posta:", self.giris_karti)
        self.email_yazisi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.email_yazisi.setGeometry(50, 120, 350, 30)
        self.email_yazisi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.giris_emaili = QLineEdit(self.giris_karti)
        self.giris_emaili.setGeometry(50, 155, 350, 55)
        self.giris_emaili.setPlaceholderText("E-posta adresinizi girin...")
        self.giris_emaili.setStyleSheet(degiskenler.modern_lineedit_stili)
        
        # Şifre alanı
        self.sifre_yazisi = QLabel("🔒 Şifre:", self.giris_karti)
        self.sifre_yazisi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.sifre_yazisi.setGeometry(50, 240, 350, 30)
        self.sifre_yazisi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.giris_sifresi = QLineEdit(self.giris_karti)
        self.giris_sifresi.setGeometry(50, 275, 350, 55)
        self.giris_sifresi.setPlaceholderText("Şifrenizi girin...")
        self.giris_sifresi.setEchoMode(QLineEdit.Password)
        self.giris_sifresi.setStyleSheet(degiskenler.modern_lineedit_stili)
        
        # Giriş Butonu
        self.giris_butonu = GlowButton("🚀 Giriş Yap", self.giris_karti)
        self.giris_butonu.setGeometry(100, 380, 250, 65)
        self.giris_butonu.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.giris_butonu.setStyleSheet(degiskenler.modern_buton_stili)
        self.giris_butonu.clicked.connect(self.giris_yap)

    def kayit_kartini_baslat(self):
        # Kayıt kartı
        self.kayit_karti = FloatingCard(self)
        self.kayit_karti.setGeometry(950, 200, 450, 650)
        self.kayit_karti.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Kayıt Ol başlığı
        kayit_basligi = QLabel("✨ Kayıt Ol", self.kayit_karti)
        kayit_basligi.setFont(QFont("Segoe UI", 24, QFont.Bold))
        kayit_basligi.setAlignment(Qt.AlignCenter)
        kayit_basligi.setGeometry(50, 20, 350, 50)
        kayit_basligi.setStyleSheet("color: white; background: transparent; border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3);")
        
        # Email ve Şifre Alanları
        self.kayit_emaili = QLineEdit(self.kayit_karti)
        self.kayit_emaili.setGeometry(50, 90, 350, 50)
        self.kayit_emaili.setPlaceholderText("📧 E-posta adresiniz...")
        self.kayit_emaili.setStyleSheet(degiskenler.modern_lineedit_stili)
        
        self.kayit_sifresi = QLineEdit(self.kayit_karti)
        self.kayit_sifresi.setGeometry(50, 160, 350, 50)
        self.kayit_sifresi.setPlaceholderText("🔒 Şifreniz (min 6 karakter)...")
        self.kayit_sifresi.setEchoMode(QLineEdit.Password)
        self.kayit_sifresi.setStyleSheet(degiskenler.modern_lineedit_stili)
        
        # Kişisel Bilgi Alanı
        kisisel_bilgi = QLabel("👤 Kişisel Bilgiler", self.kayit_karti)
        kisisel_bilgi.setFont(QFont("Segoe UI", 14, QFont.Bold))
        kisisel_bilgi.setGeometry(50, 230, 350, 30)
        kisisel_bilgi.setStyleSheet("color: white; background: transparent; border: none;")
        
        # Cinsiyet
        self.cinsiyet_kutusu = QComboBox(self.kayit_karti)
        self.cinsiyet_kutusu.addItems(["👤 Cinsiyet", "👩 Kadın", "👨 Erkek"])
        self.cinsiyet_kutusu.setGeometry(50, 270, 165, 45)
        self.cinsiyet_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Meslek
        self.meslek_kutusu = QComboBox(self.kayit_karti)
        meslek_ogeleri = ["💼 Meslek"] + degiskenler.meslek_listesi
        self.meslek_kutusu.addItems(meslek_ogeleri)
        self.meslek_kutusu.setGeometry(235, 270, 165, 45)
        self.meslek_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Eğitim
        self.egitim_kutusu = QComboBox(self.kayit_karti)
        egitim_ogeleri = ["🎓 Eğitim"] + degiskenler.egitim_listesi
        self.egitim_kutusu.addItems(egitim_ogeleri)
        self.egitim_kutusu.setGeometry(50, 335, 165, 45)
        self.egitim_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Yaş
        self.yas_kutusu = QComboBox(self.kayit_karti)
        yas_ogeleri = ["🎂 Yaş"] + degiskenler.yas_listesi
        self.yas_kutusu.addItems(yas_ogeleri)
        self.yas_kutusu.setGeometry(235, 335, 165, 45)
        self.yas_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Boy
        self.boy_kutusu = QComboBox(self.kayit_karti)
        boy_ogeleri = ["📏 Boy"] + degiskenler.boy_listesi
        self.boy_kutusu.addItems(boy_ogeleri)
        self.boy_kutusu.setGeometry(50, 400, 165, 45)
        self.boy_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Kilo
        self.kilo_kutusu = QComboBox(self.kayit_karti)
        kilo_ogeleri = ["⚖️ Kilo"] + degiskenler.kilo_listesi
        self.kilo_kutusu.addItems(kilo_ogeleri)
        self.kilo_kutusu.setGeometry(235, 400, 165, 45)
        self.kilo_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Register button
        self.kayit_butonu = GlowButton("🌟 Hesap Oluştur", self.kayit_karti)
        self.kayit_butonu.setGeometry(100, 500, 250, 65)
        self.kayit_butonu.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.kayit_butonu.setStyleSheet(degiskenler.modern_buton_stili_2)
        self.kayit_butonu.clicked.connect(self.kayit_ol)

    def mode_butonunu_baslat(self):
        self.mod_butonu = GlowButton("☀️ Gündüz Modu", self)
        self.mod_butonu.setGeometry(50, 50, 200, 60)
        self.mod_butonu.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.mod_butonu.setStyleSheet(degiskenler.mode_button_style)
        self.mod_butonu.clicked.connect(self.mod_degistir)

    def animasyonu_hazirla(self):
        # Kartlar için dalgalanma animasyonunu başlat
        QTimer.singleShot(500, self.giris_karti.start_floating)
        QTimer.singleShot(700, self.kayit_karti.start_floating)
        
        # Başlık animasyonu
        self.baslik_animasyonu = QPropertyAnimation(self.baslik_yazisi, b"pos")
        self.baslik_animasyonu.setDuration(1000)
        self.baslik_animasyonu.setEasingCurve(QEasingCurve.OutBounce)

        # Başlık parıltıları
        self.baslik_parlama_animasyonu = QPropertyAnimation(self.baslik_yazisi.graphicsEffect(), b"blurRadius")
        self.baslik_parlama_animasyonu.setDuration(2000)
        self.baslik_parlama_animasyonu.setStartValue(10)
        self.baslik_parlama_animasyonu.setEndValue(30)
        self.baslik_parlama_animasyonu.setLoopCount(-1)
        self.baslik_parlama_animasyonu.setEasingCurve(QEasingCurve.InOutSine)
        # Hata alınan satır düzeltildi:
        self.baslik_parlama_animasyonu.setDirection(QAbstractAnimation.Direction.Forward) 
        
        self.baslik_parlama_animasyonu.start()
        
        baslangic_pozisyonu = QPoint(200, -100)
        bitis_pozisyonu = QPoint(200, 50)
        self.baslik_animasyonu.setStartValue(baslangic_pozisyonu)
        self.baslik_animasyonu.setEndValue(bitis_pozisyonu)
        self.baslik_animasyonu.start()

    def mod_degistir(self):
        self.gece_modu = not self.gece_modu
        
        if self.gece_modu:
            self.mod_butonu.setText("☀️ Gündüz Modu")
            # Karanlık Temayı uygula
            koyu_kart_stili = """
            QFrame {
                background: rgba(26, 32, 44, 0.8);
                border: 2px solid rgba(100, 100, 100, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
            """
            self.giris_karti.setStyleSheet(koyu_kart_stili)
            self.kayit_karti.setStyleSheet(koyu_kart_stili)

        else:
            self.mod_butonu.setText("🌙 Gece Modu")
            # Aydınlık Temayı uygula
            aydinlik_kart_stili = """
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
            """
            self.giris_karti.setStyleSheet(aydinlik_kart_stili)
            self.kayit_karti.setStyleSheet(aydinlik_kart_stili)

    def uygulamayi_kapat(self):
        cevap = QMessageBox.question(self, 'Çıkış', 
                                   'Uygulamadan çıkmak istediğinizden emin misiniz?',
                                   QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.close()
            sys.exit()

    def giris_yap(self):
        email = self.giris_emaili.text()
        sifre = self.giris_sifresi.text()
        
        if not email or not sifre:
            self.mesaji_goster("Hata", "Lütfen tüm alanları doldurun!", "error")
            return
        
        from veritabani import giris_kontrol

        if giris_kontrol(email, sifre):
            degiskenler.giris_durumu = True
            degiskenler.giris_yapan_email = email
            self.mesaji_goster("Başarılı", "Giriş başarılı! Hoş geldiniz.", "success")
            
            # Solma Animasyonu
            self.solma_animasyonu = QPropertyAnimation(self, b"windowOpacity")
            self.solma_animasyonu.setDuration(500)
            self.solma_animasyonu.setStartValue(1.0)
            self.solma_animasyonu.setEndValue(0.0)
            self.solma_animasyonu.finished.connect(self.chat_ekranini_ac)
            self.solma_animasyonu.start()
        else:
            self.mesaji_goster("Hata", "E-posta veya şifre hatalı!", "error")

    def chat_ekranini_ac(self):
        from chatEkrani import ChatWindow
        self.chat_ekrani = ChatWindow()
        self.hide()
        self.chat_ekrani.show()

    def kayit_ol(self):
        email = self.kayit_emaili.text()
        sifre = self.kayit_sifresi.text()
        
        if not email or not sifre:
            self.mesaji_goster("Hata", "E-posta ve şifre alanları zorunludur!", "error")
            return
            
        if self.cinsiyet_kutusu.currentIndex() == 0:
            self.mesaji_goster("Hata", "Lütfen cinsiyetinizi seçin!", "error")
            return
        
        from veritabani import kullanici_ekle, kullanici_var_mi
        from email_yonetimi import dogrulama_kodu_gonder

        if kullanici_var_mi(email):
            self.mesaji_goster("Hata", "Bu e-posta adresi zaten kayıtlı!", "error")
            return

        if not any(email.endswith(domain) for domain in ["@gmail.com", "@hotmail.com", "@outlook.com"]):
            self.mesaji_goster("Hata", "Geçerli bir e-posta adresi girin!", "error")
            return
            
        if len(sifre) < 6:
            self.mesaji_goster("Hata", "Şifre en az 6 karakter olmalıdır!", "error")
            return
            
        if " " in email or " " in sifre:
            self.mesaji_goster("Hata", "E-posta ve şifrede boşluk kullanmayın!", "error")
            return

        # Email verification
        gmail_adresi = os.getenv("EMAIL_ADRESI")
        gmail_sifresi = os.getenv("EMAIL_SIFRE")
        kod = dogrulama_kodu_gonder(email, gmail_adresi, gmail_sifresi)

        if not kod:
            self.mesaji_goster("Hata", "Doğrulama kodu gönderilemedi!", "error")
            return

        girilen_kod, ok = QInputDialog.getText(self, "📧 E-posta Doğrulama", 
                                             "E-posta adresinize gönderilen doğrulama kodunu girin:")
        
        if ok and girilen_kod == kod:
            kullanici_ekle(
                email, sifre,
                self.cinsiyet_kutusu.currentText().replace("👩 ", "").replace("👨 ", ""),
                self.meslek_kutusu.currentText().replace("💼 ", ""),
                self.egitim_kutusu.currentText().replace("🎓 ", ""),
                self.yas_kutusu.currentText().replace("🎂 ", ""),
                self.boy_kutusu.currentText().replace("📏 ", ""),
                self.kilo_kutusu.currentText().replace("⚖️ ", "")
            )
            
            degiskenler.giris_durumu = True
            degiskenler.giris_yapan_email = email
            self.mesaji_goster("Başarılı", "Kayıt başarılı! Hoş geldiniz.", "success")
            
            # Fade out animation
            self.solma_animasyonu = QPropertyAnimation(self, b"windowOpacity")
            self.solma_animasyonu.setDuration(500)
            self.solma_animasyonu.setStartValue(1.0)
            self.solma_animasyonu.setEndValue(0.0)
            self.solma_animasyonu.finished.connect(self.chat_ekranini_ac)
            self.solma_animasyonu.start()
        else:
            self.mesaji_goster("Hata", "Doğrulama kodu yanlış!", "error")

    def mesaji_goster(self, baslik, mesaj, mesaj_tipi):
        mesaj_kutusu = QMessageBox(self)
        mesaj_kutusu.setWindowTitle(baslik)
        mesaj_kutusu.setText(mesaj)
        
        if mesaj_tipi == "success":
            mesaj_kutusu.setIcon(QMessageBox.Information)
            mesaj_kutusu.setStyleSheet("""
                QMessageBox {
                    background-color: #d4edda;
                    color: #155724;
                    border: 2px solid #c3e6cb;
                    border-radius: 10px;
                }
                QMessageBox QLabel {
                    color: #155724;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)
        else:
            mesaj_kutusu.setIcon(QMessageBox.Critical)
            mesaj_kutusu.setStyleSheet("""
                QMessageBox {
                    background-color: #f8d7da;
                    color: #721c24;
                    border: 2px solid #f5c6cb;
                    border-radius: 10px;
                }
                QMessageBox QLabel {
                    color: #721c24;
                    font-size: 14px;
                }
                QMessageBox QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 5px;
                    font-weight: bold;
                }
            """)
        
        mesaj_kutusu.exec_()

    def fare_tiklamasi(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def fare_suruklemesi(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            self.move(self.pos() + event.globalPos() - self.drag_start_position)
            self.drag_start_position = event.globalPos()

def ana_ekrani_goster(acilis_ekrani, ekran): # Yeni yardımcı fonksiyon
    acilis_ekrani.close()  # Sıçrama ekranını kapat
    ekran.show()   # Ana pencereyi göster (tam ekran yerine show kullandım, tam ekran istersen window.showFullScreen() kullanabilirsin)

def main():
    uygulama = QApplication(sys.argv)
    uygulama.setStyle('Fusion')  # Modern görünüm
    
    # Uygulama İkonunu ayarla
    uygulama.setWindowIcon(QIcon("robot.png")) #<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Hilmy Abiyyu A. - Flaticon</a>

    acilis_ekran_ikonu = QPixmap("robot.png")  #<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Hilmy Abiyyu A. - Flaticon</a>
    acilis_ekrani = QSplashScreen(acilis_ekran_ikonu, Qt.WindowType.WindowStaysOnTopHint)
    ekranlar = QApplication.screens()
    if len(ekranlar) > 1:
        second_screen = ekranlar[-1] # Son ekranı ikinci ekran olarak kabul et
        acilis_ekrani.move(second_screen.geometry().center() - acilis_ekrani.rect().center())
        
    acilis_ekrani.show() # açılış ekranını göster(robot ikonu)

    ekran = LoginWindow()
    ekran.hide()
    
    kaybolma_animasyonu = QPropertyAnimation(ekran, b"windowOpacity")
    kaybolma_animasyonu.setDuration(1000)
    kaybolma_animasyonu.setStartValue(0.0)
    kaybolma_animasyonu.setEndValue(1.0)
    kaybolma_animasyonu.start()

    QTimer.singleShot(2000, lambda: ana_ekrani_goster(acilis_ekrani, ekran))
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    main()