import sys
import os
import degiskenler
from dotenv import load_dotenv
from classes import *

load_dotenv()

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

class LoginRegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle("Alışveriş Asistanı - Premium Edition")
        self.setWindowIcon(QIcon("robot.png"))
        self.gece_modu = False
        
        # Set window flags for modern look
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.initUI()
        self.setup_animations()

    def initUI(self):
        # Main container with animated background
        self.main_container = QWidget(self)
        self.setCentralWidget(self.main_container)
        
        # Animated background
        self.background = AnimatedBackground(self)
        self.background.setGeometry(0, 0, 1600, 900)
        
        # Title with glow effect
        self.title_label = QLabel("✨ Alışveriş Asistanı ✨", self)
        self.title_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(200, 50, 1200, 80)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            }
        """)
        
        # Subtitle
        self.subtitle = QLabel("Premium alışveriş deneyimi için giriş yapın", self)
        self.subtitle.setFont(QFont("Segoe UI", 16))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setGeometry(200, 130, 1200, 40)
        self.subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
        """)
        
        # Window controls
        self.init_window_controls()
        
        # Login and register cards
        self.init_login_card()
        self.init_register_card()
        
        # Mode toggle button
        self.init_mode_button()

    def init_window_controls(self):
        # Close button
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setGeometry(1540, 20, 40, 40)
        self.close_btn.setStyleSheet("""
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
        self.close_btn.clicked.connect(self.close_application)
        
        # Minimize button
        self.min_btn = QPushButton("—", self)
        self.min_btn.setGeometry(1490, 20, 40, 40)
        self.min_btn.setStyleSheet("""
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
        self.min_btn.clicked.connect(self.showMinimized)

    def init_login_card(self):
        # Login card
        self.login_card = FloatingCard(self)
        self.login_card.setGeometry(200, 250, 450, 500)
        self.login_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Login title
        login_title = QLabel("🔐 Giriş Yap", self.login_card)
        login_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setGeometry(50, 30, 350, 50)
        login_title.setStyleSheet("color: white; background: transparent; border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3);")
        
        # Email field
        self.email_label = QLabel("📧 E-posta:", self.login_card)
        self.email_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.email_label.setGeometry(50, 120, 350, 30)
        self.email_label.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.login_email = QLineEdit(self.login_card)
        self.login_email.setGeometry(50, 155, 350, 55)
        self.login_email.setPlaceholderText("E-posta adresinizi girin...")
        self.login_email.setStyleSheet(degiskenler.modern_lineedit_style)
        
        # Password field
        self.password_label = QLabel("🔒 Şifre:", self.login_card)
        self.password_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.password_label.setGeometry(50, 240, 350, 30)
        self.password_label.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.login_password = QLineEdit(self.login_card)
        self.login_password.setGeometry(50, 275, 350, 55)
        self.login_password.setPlaceholderText("Şifrenizi girin...")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet(degiskenler.modern_lineedit_style)
        
        # Login button
        self.login_btn = GlowButton("🚀 Giriş Yap", self.login_card)
        self.login_btn.setGeometry(100, 380, 250, 65)
        self.login_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.login_btn.setStyleSheet(degiskenler.premium_button_style)
        self.login_btn.clicked.connect(self.giris_yap)

    def init_register_card(self):
        # Register card
        self.register_card = FloatingCard(self)
        self.register_card.setGeometry(950, 200, 450, 650)
        self.register_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: none;
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Register title
        register_title = QLabel("✨ Kayıt Ol", self.register_card)
        register_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        register_title.setAlignment(Qt.AlignCenter)
        register_title.setGeometry(50, 20, 350, 50)
        register_title.setStyleSheet("color: white; background: transparent; border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3);")
        
        # Email and password fields
        self.register_email = QLineEdit(self.register_card)
        self.register_email.setGeometry(50, 90, 350, 50)
        self.register_email.setPlaceholderText("📧 E-posta adresiniz...")
        self.register_email.setStyleSheet(degiskenler.modern_lineedit_style)
        
        self.register_password = QLineEdit(self.register_card)
        self.register_password.setGeometry(50, 160, 350, 50)
        self.register_password.setPlaceholderText("🔒 Şifreniz (min 6 karakter)...")
        self.register_password.setEchoMode(QLineEdit.Password)
        self.register_password.setStyleSheet(degiskenler.modern_lineedit_style)
        
        # Personal info section
        personal_info = QLabel("👤 Kişisel Bilgiler", self.register_card)
        personal_info.setFont(QFont("Segoe UI", 14, QFont.Bold))
        personal_info.setGeometry(50, 230, 350, 30)
        personal_info.setStyleSheet("color: white; background: transparent; border: none;")
        
        # Gender
        self.gender_combo = QComboBox(self.register_card)
        self.gender_combo.addItems(["👤 Cinsiyet", "👩 Kadın", "👨 Erkek"])
        self.gender_combo.setGeometry(50, 270, 165, 45)
        self.gender_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Profession
        self.profession_combo = QComboBox(self.register_card)
        profession_items = ["💼 Meslek"] + degiskenler.meslek_listesi
        self.profession_combo.addItems(profession_items)
        self.profession_combo.setGeometry(235, 270, 165, 45)
        self.profession_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Education
        self.education_combo = QComboBox(self.register_card)
        education_items = ["🎓 Eğitim"] + degiskenler.egitim_listesi
        self.education_combo.addItems(education_items)
        self.education_combo.setGeometry(50, 335, 165, 45)
        self.education_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Age
        self.age_combo = QComboBox(self.register_card)
        age_items = ["🎂 Yaş"] + degiskenler.yas_listesi
        self.age_combo.addItems(age_items)
        self.age_combo.setGeometry(235, 335, 165, 45)
        self.age_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Height
        self.height_combo = QComboBox(self.register_card)
        height_items = ["📏 Boy"] + degiskenler.boy_listesi
        self.height_combo.addItems(height_items)
        self.height_combo.setGeometry(50, 400, 165, 45)
        self.height_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Weight
        self.weight_combo = QComboBox(self.register_card)
        weight_items = ["⚖️ Kilo"] + degiskenler.kilo_listesi
        self.weight_combo.addItems(weight_items)
        self.weight_combo.setGeometry(235, 400, 165, 45)
        self.weight_combo.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Register button
        self.register_btn = GlowButton("🌟 Hesap Oluştur", self.register_card)
        self.register_btn.setGeometry(100, 500, 250, 65)
        self.register_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.register_btn.setStyleSheet(degiskenler.premium_button_style_2)
        self.register_btn.clicked.connect(self.kayit_ol)

    def init_mode_button(self):
        self.mode_btn = GlowButton("🌙 Gece Modu", self)
        self.mode_btn.setGeometry(50, 50, 200, 60)
        self.mode_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.mode_btn.setStyleSheet(degiskenler.mode_button_style)
        self.mode_btn.clicked.connect(self.toggle_mode)

    def setup_animations(self):
        # Start floating animations for cards
        QTimer.singleShot(500, self.login_card.start_floating)
        QTimer.singleShot(700, self.register_card.start_floating)
        
        # Title animation
        self.title_animation = QPropertyAnimation(self.title_label, b"pos")
        self.title_animation.setDuration(1000)
        self.title_animation.setEasingCurve(QEasingCurve.OutBounce)

        # Title glow animation
        self.title_glow_animation = QPropertyAnimation(self.title_label.graphicsEffect(), b"blurRadius")
        self.title_glow_animation.setDuration(2000)
        self.title_glow_animation.setStartValue(10)
        self.title_glow_animation.setEndValue(30)
        self.title_glow_animation.setLoopCount(-1)
        self.title_glow_animation.setEasingCurve(QEasingCurve.InOutSine)
        # Hata alınan satır düzeltildi:
        self.title_glow_animation.setDirection(QAbstractAnimation.Direction.Forward) 
        
        self.title_glow_animation.start()
        
        start_pos = QPoint(200, -100)
        end_pos = QPoint(200, 50)
        self.title_animation.setStartValue(start_pos)
        self.title_animation.setEndValue(end_pos)
        self.title_animation.start()

    def toggle_mode(self):
        self.gece_modu = not self.gece_modu
        
        if self.gece_modu:
            self.mode_btn.setText("☀️ Gündüz Modu")
            # Apply dark theme styles
            self.apply_dark_theme()
        else:
            self.mode_btn.setText("🌙 Gece Modu")
            # Apply light theme styles
            self.apply_light_theme()

    def apply_dark_theme(self):
        # Update card styles for dark mode
        dark_card_style = """
            QFrame {
                background: rgba(26, 32, 44, 0.8);
                border: 2px solid rgba(100, 100, 100, 0.3);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """
        self.login_card.setStyleSheet(dark_card_style)
        self.register_card.setStyleSheet(dark_card_style)

    def apply_light_theme(self):
        # Update card styles for light mode
        light_card_style = """
            QFrame {
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                backdrop-filter: blur(20px);
            }
        """
        self.login_card.setStyleSheet(light_card_style)
        self.register_card.setStyleSheet(light_card_style)

    def close_application(self):
        reply = QMessageBox.question(self, 'Çıkış', 
                                   'Uygulamadan çıkmak istediğinizden emin misiniz?',
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
            sys.exit()

    def giris_yap(self):
        email = self.login_email.text()
        sifre = self.login_password.text()
        
        if not email or not sifre:
            self.show_message("Hata", "Lütfen tüm alanları doldurun!", "error")
            return
            
        from chatEkrani import ChatWindow
        from veritabani import giris_kontrol

        if giris_kontrol(email, sifre):
            degiskenler.giris_durumu = True
            degiskenler.giris_yapan_email = email
            self.show_message("Başarılı", "Giriş başarılı! Hoş geldiniz.", "success")
            
            # Fade out animation before switching
            self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
            self.fade_out_animation.setDuration(500)
            self.fade_out_animation.setStartValue(1.0)
            self.fade_out_animation.setEndValue(0.0)
            self.fade_out_animation.finished.connect(self.open_chat_window)
            self.fade_out_animation.start()
        else:
            self.show_message("Hata", "E-posta veya şifre hatalı!", "error")

    def open_chat_window(self):
        from chatEkrani import ChatWindow
        self.chat_window = ChatWindow()
        self.hide()
        self.chat_window.show()

    def kayit_ol(self):
        email = self.register_email.text()
        sifre = self.register_password.text()
        
        if not email or not sifre:
            self.show_message("Hata", "E-posta ve şifre alanları zorunludur!", "error")
            return
            
        if self.gender_combo.currentIndex() == 0:
            self.show_message("Hata", "Lütfen cinsiyetinizi seçin!", "error")
            return
            
        from chatEkrani import ChatWindow 
        from veritabani import kullanici_ekle, kullanici_var_mi
        from email_yonetimi import dogrulama_kodu_gonder

        if kullanici_var_mi(email):
            self.show_message("Hata", "Bu e-posta adresi zaten kayıtlı!", "error")
            return

        if not any(email.endswith(domain) for domain in ["@gmail.com", "@hotmail.com", "@outlook.com"]):
            self.show_message("Hata", "Geçerli bir e-posta adresi girin!", "error")
            return
            
        if len(sifre) < 6:
            self.show_message("Hata", "Şifre en az 6 karakter olmalıdır!", "error")
            return
            
        if " " in email or " " in sifre:
            self.show_message("Hata", "E-posta ve şifrede boşluk kullanmayın!", "error")
            return

        # Email verification
        gmail_adresi = os.getenv("EMAIL_ADRESI")
        gmail_sifresi = os.getenv("EMAIL_SIFRE")
        kod = dogrulama_kodu_gonder(email, gmail_adresi, gmail_sifresi)

        if not kod:
            self.show_message("Hata", "Doğrulama kodu gönderilemedi!", "error")
            return

        girilen_kod, ok = QInputDialog.getText(self, "📧 E-posta Doğrulama", 
                                             "E-posta adresinize gönderilen doğrulama kodunu girin:")
        
        if ok and girilen_kod == kod:
            kullanici_ekle(
                email, sifre,
                self.gender_combo.currentText().replace("👩 ", "").replace("👨 ", ""),
                self.profession_combo.currentText().replace("💼 ", ""),
                self.education_combo.currentText().replace("🎓 ", ""),
                self.age_combo.currentText().replace("🎂 ", ""),
                self.height_combo.currentText().replace("📏 ", ""),
                self.weight_combo.currentText().replace("⚖️ ", "")
            )
            
            degiskenler.giris_durumu = True
            degiskenler.giris_yapan_email = email
            self.show_message("Başarılı", "Kayıt başarılı! Hoş geldiniz.", "success")
            
            # Fade out animation
            self.fade_out_animation = QPropertyAnimation(self, b"windowOpacity")
            self.fade_out_animation.setDuration(500)
            self.fade_out_animation.setStartValue(1.0)
            self.fade_out_animation.setEndValue(0.0)
            self.fade_out_animation.finished.connect(self.open_chat_window)
            self.fade_out_animation.start()
        else:
            self.show_message("Hata", "Doğrulama kodu yanlış!", "error")

    def show_message(self, title, message, msg_type):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setStyleSheet("""
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
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setStyleSheet("""
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
        
        msg_box.exec_()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            self.move(self.pos() + event.globalPos() - self.drag_start_position)
            self.drag_start_position = event.globalPos()

def show_main_window(splash, window): # Yeni yardımcı fonksiyon
    splash.close()  # Splash ekranını kapat
    window.show()   # Ana pencereyi göster (tam ekran yerine show kullandım, tam ekran istersen window.showFullScreen() kullanabilirsin)

def main():
    uygulama = QApplication(sys.argv)
    uygulama.setStyle('Fusion')  # Modern look
    
    # Set application icon
    uygulama.setWindowIcon(QIcon("robot.png"))

    splash_pixmap = QPixmap("robot.png")  
    splash = QSplashScreen(splash_pixmap, Qt.WindowType.WindowStaysOnTopHint)
    screens = QApplication.screens()
    if len(screens) > 1:
        second_screen = screens[-1] # Son ekranı ikinci ekran olarak kabul et
        splash.move(second_screen.geometry().center() - splash.rect().center())
        
    splash.show() # Splash ekranını göste

    pencere = LoginRegisterWindow()
    pencere.hide()
    
    # Fade in animation
    fade_in = QPropertyAnimation(pencere, b"windowOpacity")
    fade_in.setDuration(1000)
    fade_in.setStartValue(0.0)
    fade_in.setEndValue(1.0)
    fade_in.start()

    QTimer.singleShot(2000, lambda: show_main_window(splash, pencere))
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    main()