import sys
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import degiskenler

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

class LoginRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1400, 900)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))

        self.initUI()

    def initUI(self):
        self.yazi = QLabel("Alışveriş asistanına hoşgeldiniz devam etmek için lütfen giriş yapın",self)
        self.yazi.setFont(degiskenler.baslik_fontu)
        self.yazi.setGeometry(200,100,1200,100)
        
        self.kapat_butonu = QPushButton("Çıkış Yap",self)
        self.kapat_butonu.setGeometry(100,700,200,100)
        self.kapat_butonu.setFont(degiskenler.buton_fontu)
        self.kapat_butonu.clicked.connect(self.cikis_yap)

        self.initLoginForm()
        self.initRegisterForm()

    def initLoginForm(self):
        self.giris_butonu = QPushButton("Giriş Yap",self)
        self.giris_butonu.setGeometry(400,250,200,100)
        self.giris_butonu.setFont(degiskenler.buton_fontu)
        self.giris_butonu.clicked.connect(self.giris_yap) 

        self.email_yazisi = QLabel("Lütfen emailinizi giriniz: ",self)
        self.email_yazisi.setFont(degiskenler.yazi_fontu)
        self.email_yazisi.setGeometry(170,370,200,40)

        self.giris_email_kutusu = QLineEdit(self)
        self.giris_email_kutusu.setGeometry(375,370,250,50)

        self.sifre_yazisi = QLabel("Lütfen şifrenizi giriniz: ",self)
        self.sifre_yazisi.setFont(degiskenler.yazi_fontu)
        self.sifre_yazisi.setGeometry(180,470,200,40)

        self.giris_sifre_kutusu = QLineEdit(self)
        self.giris_sifre_kutusu.setGeometry(375,470,250,50)

    def initRegisterForm(self):
        self.kayit_butonu = QPushButton("Kayıt Ol",self)
        self.kayit_butonu.setGeometry(950,250,200,100)
        self.kayit_butonu.setFont(degiskenler.buton_fontu)
        self.kayit_butonu.clicked.connect(self.kayit_ol)

        self.kayit_email_kutusu = QLineEdit(self)
        self.kayit_email_kutusu.setGeometry(925,370,250,50)

        self.kayit_sifre_kutusu = QLineEdit(self)
        self.kayit_sifre_kutusu.setGeometry(925,470,250,50)

        self.cinsiyet_yazisi = QLabel("Cinsiyetiniz: ",self)
        self.cinsiyet_yazisi.setFont(degiskenler.yazi_fontu)
        self.cinsiyet_yazisi.setGeometry(775,550,100,30)

        self.cinsiyet_kutusu = QComboBox(self)
        self.cinsiyet_kutusu.addItems(["Kadın","Erkek"])
        self.cinsiyet_kutusu.setGeometry(880,540,150,50)
        self.cinsiyet_kutusu.setFont(degiskenler.yazi_fontu)

        self.meslek_yazisi = QLabel("Mesleğiniz: ",self)
        self.meslek_yazisi.setFont(degiskenler.yazi_fontu)
        self.meslek_yazisi.setGeometry(775,650,100,30)

        self.meslek_kutusu = QComboBox(self)
        self.meslek_kutusu.addItems(degiskenler.meslek_listesi)
        self.meslek_kutusu.setGeometry(880,640,150,50)
        self.meslek_kutusu.setFont(degiskenler.yazi_fontu)

        self.egitim_yazisi = QLabel("    Eğitim\nDurumunuz: ",self)
        self.egitim_yazisi.setFont(degiskenler.yazi_fontu)
        self.egitim_yazisi.setGeometry(770,740,100,50)

        self.egitim_kutusu = QComboBox(self)
        self.egitim_kutusu.addItems(degiskenler.egitim_listesi)
        self.egitim_kutusu.setGeometry(880,740,150,50)
        self.egitim_kutusu.setFont(degiskenler.yazi_fontu)

        self.yas_yazisi = QLabel("    Yaş\nAralığınız: ",self)
        self.yas_yazisi.setFont(degiskenler.yazi_fontu)
        self.yas_yazisi.setGeometry(1050,540,100,50)

        self.yas_kutusu = QComboBox(self)
        self.yas_kutusu.addItems(degiskenler.yas_listesi)
        self.yas_kutusu.setGeometry(1150,540,150,50)
        self.yas_kutusu.setFont(degiskenler.yazi_fontu)

        self.boy_yazisi = QLabel("    Boy\nAralığınız: ",self)
        self.boy_yazisi.setFont(degiskenler.yazi_fontu)
        self.boy_yazisi.setGeometry(1050,650,100,50)

        self.boy_kutusu = QComboBox(self)
        self.boy_kutusu.addItems(degiskenler.boy_listesi)
        self.boy_kutusu.setGeometry(1150,650,150,50)
        self.boy_kutusu.setFont(degiskenler.yazi_fontu)

        self.kilo_yazisi = QLabel("    Kilo\nAralığınız: ",self)
        self.kilo_yazisi.setFont(degiskenler.yazi_fontu)
        self.kilo_yazisi.setGeometry(1050,750,100,50)

        self.kilo_kutusu = QComboBox(self)
        self.kilo_kutusu.addItems(degiskenler.kilo_listesi)
        self.kilo_kutusu.setGeometry(1150,750,150,50)
        self.kilo_kutusu.setFont(degiskenler.yazi_fontu)

    def cikis_yap(self):
        soru = QMessageBox().question(self,"Çıkış yap","Uygulamadan çıkmak istediğinize emin misiniz?",QMessageBox.Yes | QMessageBox.No) 
        if soru == QMessageBox.Yes:
            self.close()
            sys.exit()  
  
    def giris_yap(self):
        email = self.giris_email_kutusu.text().strip().lower()
        sifre = self.giris_sifre_kutusu.text().strip()
        from veriYonetimi import giris_kontrol
        from chat import ChatWindow

        if giris_kontrol(email,sifre):
            degiskenler.giris_durumu = True
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
        from veriYonetimi import kullanici_var_mi,kullanici_ekle
        from chat import ChatWindow 
        
        if kullanici_var_mi(email):
            uyari = QMessageBox()
            uyari.setWindowTitle("Kayıt Başarısız")
            uyari.setText("Bu maile ait kayıtlı bir hesap bulunmaktadır")
            uyari.exec_()
        elif any(email.endswith(kelime) for kelime in ["@gmail.com", "@hotmail.com", "@outlook.com"]) and len(sifre) >= 6 and " " not in email and " " not in sifre: 
            kullanici_ekle(email,sifre,profil={"cinsiyet": self.cinsiyet_kutusu.currentText(),
                                                "meslek": self.meslek_kutusu.currentText(),
                                                "egitim": self.egitim_kutusu.currentText(),
                                                "yas": self.yas_kutusu.currentText(),
                                                "boy": self.boy_kutusu.currentText(),
                                                "kilo": self.kilo_kutusu.currentText()})
            degiskenler.giris_durumu = True
            self.konusma_penceresi = ChatWindow()
            self.hide()
            self.konusma_penceresi.show()
        else:
            uyari = QMessageBox()
            uyari.setWindowTitle("Kayıt Başarısız")
            uyari.setText("Lütfen geçerli bir e-posta adresi ve en az 6 haneli bir şifre girin.Ayrıca boşluk karakterini kullanmayın")
            uyari.exec_()              

def main():
    uygulama = QApplication(sys.argv)
    pencere = LoginRegisterWindow()
    pencere.show()
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    main()        