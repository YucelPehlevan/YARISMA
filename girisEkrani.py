import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import degiskenler
from dotenv import load_dotenv

load_dotenv()

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

class LoginRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))
        self.gece_modu = False

        self.initUI()

    def initUI(self):
        self.yazi = QLabel("Alışveriş asistanına hoşgeldiniz devam etmek için lütfen giriş yapın",self)
        self.yazi.setFont(degiskenler.baslik_fontu)
        self.yazi.setGeometry(300,100,1200,100)
        
        self.cikis_butonu = QPushButton("Çıkış Yap",self)
        self.cikis_butonu.setGeometry(100,700,200,100)
        self.cikis_butonu.setFont(degiskenler.buton_fontu)
        self.cikis_butonu.clicked.connect(self.cikis_yap)
        self.cikis_butonu.setStyleSheet(degiskenler.buton_stili)    

        self.mod_butonu = QPushButton("🌙 Gece Modu",self)
        self.mod_butonu.setGeometry(1350,20,200,100)
        self.mod_butonu.setFont(degiskenler.buton_fontu)
        self.mod_butonu.clicked.connect(self.mod_degistir)
        self.mod_butonu.setStyleSheet(degiskenler.buton_stili)

        self.initLoginForm()
        self.initRegisterForm()

    def initLoginForm(self):
        self.giris_butonu = QPushButton("Giriş Yap",self)
        self.giris_butonu.setGeometry(400,250,200,100)
        self.giris_butonu.setFont(degiskenler.buton_fontu)
        self.giris_butonu.clicked.connect(self.giris_yap)
        self.giris_butonu.setStyleSheet(degiskenler.buton_stili) 

        self.email_yazisi = QLabel("Email: ",self)
        self.email_yazisi.setFont(degiskenler.yazi_fontu)
        self.email_yazisi.setGeometry(310,370,200,40)

        self.giris_email_kutusu = QLineEdit(self)
        self.giris_email_kutusu.setGeometry(375,370,250,50)
        self.giris_email_kutusu.setPlaceholderText("Lütfen emailinizi bu alana girin")
        self.giris_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili)

        self.sifre_yazisi = QLabel("Şifre: ",self)
        self.sifre_yazisi.setFont(degiskenler.yazi_fontu)
        self.sifre_yazisi.setGeometry(310,470,200,40)

        self.giris_sifre_kutusu = QLineEdit(self)
        self.giris_sifre_kutusu.setGeometry(375,470,250,50)
        self.giris_sifre_kutusu.setPlaceholderText("Lütfen şifrenizi bu alana girin")
        self.giris_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili)

    def initRegisterForm(self):
        self.kayit_butonu = QPushButton("Kayıt Ol",self)
        self.kayit_butonu.setGeometry(1000,250,200,100)
        self.kayit_butonu.setFont(degiskenler.buton_fontu)
        self.kayit_butonu.clicked.connect(self.kayit_ol)
        self.kayit_butonu.setStyleSheet(degiskenler.buton_stili)

        self.kayit_email_kutusu = QLineEdit(self)
        self.kayit_email_kutusu.setGeometry(975,370,250,50)
        self.kayit_email_kutusu.setPlaceholderText("Lütfen emailinizi bu alana girin")
        self.kayit_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili)

        self.kayit_sifre_kutusu = QLineEdit(self)
        self.kayit_sifre_kutusu.setGeometry(975,470,250,50)
        self.kayit_sifre_kutusu.setPlaceholderText("Lütfen şifrenizi bu alana girin")
        self.kayit_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili)

        self.cinsiyet_yazisi = QLabel("Cinsiyetiniz: ",self)
        self.cinsiyet_yazisi.setFont(degiskenler.yazi_fontu)
        self.cinsiyet_yazisi.setGeometry(775,550,100,30)

        self.cinsiyet_kutusu = QComboBox(self)
        self.cinsiyet_kutusu.addItems(["Kadın","Erkek"])
        self.cinsiyet_kutusu.setGeometry(880,540,150,50)
        self.cinsiyet_kutusu.setFont(degiskenler.yazi_fontu)
        self.cinsiyet_kutusu.setStyleSheet(degiskenler.combobox_stili)

        self.meslek_yazisi = QLabel("Mesleğiniz: ",self)
        self.meslek_yazisi.setFont(degiskenler.yazi_fontu)
        self.meslek_yazisi.setGeometry(775,650,100,30)

        self.meslek_kutusu = QComboBox(self)
        self.meslek_kutusu.addItems(degiskenler.meslek_listesi)
        self.meslek_kutusu.setGeometry(880,640,150,50)
        self.meslek_kutusu.setFont(degiskenler.yazi_fontu)
        self.meslek_kutusu.setStyleSheet(degiskenler.combobox_stili)

        self.egitim_yazisi = QLabel("    Eğitim\nDurumunuz: ",self)
        self.egitim_yazisi.setFont(degiskenler.yazi_fontu)
        self.egitim_yazisi.setGeometry(770,740,100,50)

        self.egitim_kutusu = QComboBox(self)
        self.egitim_kutusu.addItems(degiskenler.egitim_listesi)
        self.egitim_kutusu.setGeometry(880,740,150,50)
        self.egitim_kutusu.setFont(degiskenler.yazi_fontu)
        self.egitim_kutusu.setStyleSheet(degiskenler.combobox_stili)

        self.yas_yazisi = QLabel("    Yaş\nAralığınız: ",self)
        self.yas_yazisi.setFont(degiskenler.yazi_fontu)
        self.yas_yazisi.setGeometry(1050,540,100,50)

        self.yas_kutusu = QComboBox(self)
        self.yas_kutusu.addItems(degiskenler.yas_listesi)
        self.yas_kutusu.setGeometry(1150,540,150,50)
        self.yas_kutusu.setFont(degiskenler.yazi_fontu)
        self.yas_kutusu.setStyleSheet(degiskenler.combobox_stili)

        self.boy_yazisi = QLabel("    Boy\nAralığınız: ",self)
        self.boy_yazisi.setFont(degiskenler.yazi_fontu)
        self.boy_yazisi.setGeometry(1050,650,100,50)

        self.boy_kutusu = QComboBox(self)
        self.boy_kutusu.addItems(degiskenler.boy_listesi)
        self.boy_kutusu.setGeometry(1150,650,150,50)
        self.boy_kutusu.setFont(degiskenler.yazi_fontu)
        self.boy_kutusu.setStyleSheet(degiskenler.combobox_stili)

        self.kilo_yazisi = QLabel("    Kilo\nAralığınız: ",self)
        self.kilo_yazisi.setFont(degiskenler.yazi_fontu)
        self.kilo_yazisi.setGeometry(1050,750,100,50)

        self.kilo_kutusu = QComboBox(self)
        self.kilo_kutusu.addItems(degiskenler.kilo_listesi)
        self.kilo_kutusu.setGeometry(1150,750,150,50)
        self.kilo_kutusu.setFont(degiskenler.yazi_fontu)
        self.kilo_kutusu.setStyleSheet(degiskenler.combobox_stili)

    def cikis_yap(self):
        soru = QMessageBox().question(self,"Çıkış yap","Uygulamadan çıkmak istediğinize emin misiniz?",QMessageBox.Yes | QMessageBox.No) 
        if soru == QMessageBox.Yes:
            self.close()
            sys.exit()

    def mod_degistir(self):
        if not self.gece_modu:
            self.gece_modu = True
            self.mod_butonu.setText("☀️ Gündüz Modu")

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
            QApplication.setPalette(palet)

            self.kayit_butonu.setStyleSheet(degiskenler.buton_stili_gece)
            self.giris_butonu.setStyleSheet(degiskenler.buton_stili_gece)
            self.mod_butonu.setStyleSheet(degiskenler.buton_stili_gece)
            self.cikis_butonu.setStyleSheet(degiskenler.buton_stili_gece)

            self.giris_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili_gece)
            self.giris_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili_gece)
            self.kayit_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili_gece)
            self.kayit_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili_gece)

            self.cinsiyet_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)
            self.meslek_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)
            self.egitim_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)
            self.yas_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)
            self.boy_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)
            self.kilo_kutusu.setStyleSheet(degiskenler.combobox_stili_gece)                              

        else:
            self.gece_modu = False
            self.mod_butonu.setText("🌙 Gece Modu")
            QApplication.setPalette(QApplication.style().standardPalette())

            self.kayit_butonu.setStyleSheet(degiskenler.buton_stili)
            self.giris_butonu.setStyleSheet(degiskenler.buton_stili)
            self.mod_butonu.setStyleSheet(degiskenler.buton_stili)
            self.cikis_butonu.setStyleSheet(degiskenler.buton_stili)

            self.giris_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili)
            self.giris_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili)
            self.kayit_email_kutusu.setStyleSheet(degiskenler.lineEdit_stili)
            self.kayit_sifre_kutusu.setStyleSheet(degiskenler.lineEdit_stili)

            self.cinsiyet_kutusu.setStyleSheet(degiskenler.combobox_stili)
            self.meslek_kutusu.setStyleSheet(degiskenler.combobox_stili)
            self.egitim_kutusu.setStyleSheet(degiskenler.combobox_stili)
            self.yas_kutusu.setStyleSheet(degiskenler.combobox_stili)
            self.boy_kutusu.setStyleSheet(degiskenler.combobox_stili)
            self.kilo_kutusu.setStyleSheet(degiskenler.combobox_stili)

    def giris_yap(self):
        email = self.giris_email_kutusu.text()
        sifre = self.giris_sifre_kutusu.text()
        from chatEkrani import ChatWindow
        from veritabani import giris_kontrol

        if giris_kontrol(email,sifre):
            degiskenler.giris_durumu = True
            degiskenler.giris_yapan_email = email
            self.konusma_penceresi = ChatWindow()
            self.hide()
            self.konusma_penceresi.show()
        else:
            uyari = QMessageBox()
            uyari.setWindowTitle("Giriş Başarısız")
            uyari.setText("E-Posta ya da şifre hatalı")
            uyari.exec_()   

    def kayit_ol(self):
        email = self.kayit_email_kutusu.text()
        sifre = self.kayit_sifre_kutusu.text()
        from chatEkrani import ChatWindow 
        from veritabani import kullanici_ekle, kullanici_var_mi
        from email_yonetimi import dogrulama_kodu_gonder

        if kullanici_var_mi(email):
            QMessageBox.warning(self, "Kayıt Başarısız", "Bu maile ait kayıtlı bir hesap bulunmaktadır.")
            return

        if any(email.endswith(kelime) for kelime in ["@gmail.com", "@hotmail.com", "@outlook.com"]) and len(sifre) >= 6 and " " not in email and " " not in sifre:
            # Şifre ve mail geçerli, şimdi doğrulama kodu gönder
            gmail_adresi = os.getenv("EMAIL_ADRESI")
            gmail_sifresi = os.getenv("EMAIL_SIFRE")
            kod = dogrulama_kodu_gonder(email, gmail_adresi, gmail_sifresi)

            if not kod:
                QMessageBox.warning(self, "Hata", "Doğrulama kodu gönderilemedi. Lütfen daha sonra tekrar deneyin.")
                return

            girilen_kod, ok = QInputDialog.getText(self, "Doğrulama", "E-posta adresinize gelen doğrulama kodunu girin:")
            if ok and girilen_kod == kod:
                # Başarılı doğrulama
                kullanici_ekle(
                    email, sifre,
                    self.cinsiyet_kutusu.currentText(),
                    self.meslek_kutusu.currentText(),
                    self.egitim_kutusu.currentText(),
                    self.yas_kutusu.currentText(),
                    self.boy_kutusu.currentText(),
                    self.kilo_kutusu.currentText()
                )
                degiskenler.giris_durumu = True
                degiskenler.giris_yapan_email = email
                self.konusma_penceresi = ChatWindow()
                self.hide()
                self.konusma_penceresi.show()
            else:
                QMessageBox.warning(self, "Hata", "Doğrulama kodu yanlış veya işlem iptal edildi.")
        else:
            QMessageBox.warning(self, "Kayıt Başarısız", "Geçerli bir e-posta ve en az 6 karakterli şifre girin. Boşluk karakteri kullanmayın.")
                        

def main():
    uygulama = QApplication(sys.argv)
    QApplication.setPalette(QApplication.style().standardPalette())
    pencere = LoginRegisterWindow()
    pencere.show()
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    main()        