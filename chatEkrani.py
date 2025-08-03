from girisEkrani import *
import re
from urundeneme import urun_grafik_goster

# Ürün verilerini import et
try:
    from urunler import telefonlar, bilgisayarlar, kameralar, kulakliklar, tabletler
    tum_urunler = telefonlar + bilgisayarlar + kameralar + kulakliklar + tabletler
except ImportError:
    print("urunler.py dosyası bulunamadı!")
    tum_urunler = []

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 1800, 950)
        self.setWindowTitle("✨ Premium Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))
        
        # Modern window style
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.kullanici_email = degiskenler.giris_yapan_email
        self.konusma_gecmisi = []
        self.chat = None
        self.gece_modu = False
        self.urunler = tum_urunler
        self.son_onerilen_urunler = []
        self.grafik_pencereleri = []
        
        try:
            self.kullanici_email = degiskenler.giris_yapan_email
            self.profil = {
                'cinsiyet': 'Belirtilmemiş',
                'yas': 'Belirtilmemiş', 
                'meslek': 'Belirtilmemiş',
                'egitim': 'Belirtilmemiş',
                'boy': 'Belirtilmemiş',
                'kilo': 'Belirtilmemiş'
            }
        except:
            self.kullanici_email = "test@example.com"
            self.profil = {}

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.typeNextChar)
        self.typing_index = 0
        self.typing_text = ""

        self.initUI()
        self.setup_animations()

    def initUI(self):
        # Main container
        self.main_container = QWidget(self)
        self.setCentralWidget(self.main_container)
        
        # Animated background
        self.background = AnimatedChatBackground(self)
        self.background.setGeometry(0, 0, 1800, 950)
        
        # Window controls
        self.init_window_controls()
        
        # Header section
        self.init_header()
        
        # Left panel (controls)
        self.init_left_panel()
        
        # Main chat area
        self.init_chat_area()

    def init_window_controls(self):
        # Close button
        self.close_btn = QPushButton("✕", self)
        self.close_btn.setGeometry(1740, 20, 40, 40)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(239, 68, 68, 0.8);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(239, 68, 68, 1);
                transform: scale(1.1);
            }
        """)
        self.close_btn.clicked.connect(self.close)
        
        # Minimize button
        self.min_btn = QPushButton("—", self)
        self.min_btn.setGeometry(1690, 20, 40, 40)
        self.min_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(251, 191, 36, 0.8);
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(251, 191, 36, 1);
            }
        """)
        self.min_btn.clicked.connect(self.showMinimized)

    def init_header(self):
        # Title
        self.title_label = QLabel("🤖 Premium AI Shopping Assistant", self)
        self.title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setGeometry(400, 30, 1000, 50)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            }
        """)
        
        # User info
        self.user_info = QLabel(f"👤 Hoş geldin, {self.kullanici_email}", self)
        self.user_info.setFont(QFont("Segoe UI", 12))
        self.user_info.setGeometry(50, 30, 300, 30)
        self.user_info.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
        """)

    def init_left_panel(self):
        # Left control panel
        self.left_panel = GlassmorphismFrame(self)
        self.left_panel.setGeometry(30, 100, 320, 800)
        self.left_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Panel title
        panel_title = QLabel("🎯 Arama Filtreleri", self.left_panel)
        panel_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        panel_title.setGeometry(20, 20, 280, 40)
        panel_title.setStyleSheet("color: white; background: transparent;")
        
        # Product type
        self.urun_label = QLabel("📱 Ürün Türü:", self.left_panel)
        self.urun_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.urun_label.setGeometry(20, 80, 280, 30)
        self.urun_label.setStyleSheet("color: white; background: transparent;")
        
        self.urun_kutusu = QComboBox(self.left_panel)
        self.urun_kutusu.addItems(degiskenler.urun_listesi)
        self.urun_kutusu.setGeometry(20, 115, 280, 50)
        self.urun_kutusu.setStyleSheet(degiskenler.modern_combobox_style)
        self.urun_kutusu.currentTextChanged.connect(self.urun_degistir)
        
        # Budget
        self.butce_label = QLabel("💰 Bütçe Aralığı:", self.left_panel)
        self.butce_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.butce_label.setGeometry(20, 185, 280, 30)
        self.butce_label.setStyleSheet("color: white; background: transparent;")
        
        self.butce_kutusu = QComboBox(self.left_panel)
        self.butce_kutusu.addItems(degiskenler.butce_listesi)
        self.butce_kutusu.setGeometry(20, 220, 280, 50)
        self.butce_kutusu.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Brand
        self.marka_label = QLabel("🏷️ Marka Tercihi:", self.left_panel)
        self.marka_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.marka_label.setGeometry(20, 290, 280, 30)
        self.marka_label.setStyleSheet("color: white; background: transparent;")
        
        self.marka_kutusu = QComboBox(self.left_panel)
        self.marka_kutusu.addItems(degiskenler.tum_markalar)
        self.marka_kutusu.setGeometry(20, 325, 280, 50)
        self.marka_kutusu.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Usage purpose
        self.kullanim_label = QLabel("🎯 Kullanım Amacı:", self.left_panel)
        self.kullanim_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.kullanim_label.setGeometry(20, 395, 280, 30)
        self.kullanim_label.setStyleSheet("color: white; background: transparent;")
        
        self.kullanim_kutusu = QComboBox(self.left_panel)
        self.kullanim_kutusu.addItems(degiskenler.tum_kullanim_amaclari)
        self.kullanim_kutusu.setGeometry(20, 430, 280, 50)
        self.kullanim_kutusu.setStyleSheet(degiskenler.modern_combobox_style)
        
        # Action buttons
        self.init_action_buttons()

    def init_action_buttons(self):
        # Previous recommendations
        self.oneri_butonu = ModernButton("📋 Önceki Öneriler", self.left_panel)
        self.oneri_butonu.setGeometry(20, 510, 280, 55)
        self.oneri_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.oneri_butonu.setStyleSheet(degiskenler.premium_button_style)
        self.oneri_butonu.clicked.connect(self.onceki_onerileri_goster)
        
        # Charts button
        self.grafik_butonu = ModernButton("📊 Grafik Göster", self.left_panel)
        self.grafik_butonu.setGeometry(20, 580, 280, 55)
        self.grafik_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.grafik_butonu.setStyleSheet(degiskenler.premium_button_style_2)
        self.grafik_butonu.clicked.connect(self.grafik_goster)
        self.grafik_butonu.setEnabled(False)
        
        # Clear chat
        self.temizleme_butonu = ModernButton("🗑️ Sohbeti Temizle", self.left_panel)
        self.temizleme_butonu.setGeometry(20, 650, 280, 55)
        self.temizleme_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.temizleme_butonu.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #ef4444, stop:1 #dc2626);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #dc2626, stop:1 #b91c1c);
            }
        """)
        self.temizleme_butonu.clicked.connect(self.sohbet_gecmisini_temizle)
        
        # Mode toggle
        self.mod_butonu = ModernButton("🌙 Gece Modu", self.left_panel)
        self.mod_butonu.setGeometry(20, 720, 135, 55)
        self.mod_butonu.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.mod_butonu.setStyleSheet(degiskenler.mode_button_style)
        self.mod_butonu.clicked.connect(self.mod_degistir)
        
        # Logout
        self.cikis_butonu = ModernButton("🚪 Çıkış", self.left_panel)
        self.cikis_butonu.setGeometry(165, 720, 135, 55)
        self.cikis_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.cikis_butonu.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #6b7280, stop:1 #4b5563);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #4b5563, stop:1 #374151);
            }
        """)
        self.cikis_butonu.clicked.connect(self.cikis_yap)

    def init_chat_area(self):
        # Chat container
        self.chat_container = GlassmorphismFrame(self)
        self.chat_container.setGeometry(380, 100, 1380, 800)
        self.chat_container.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Input area
        self.input_area = GlassmorphismFrame(self.chat_container)
        self.input_area.setGeometry(20, 20, 1340, 200)
        self.input_area.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
        """)
        
        # Input label
        input_label = QLabel("💬 Sorununuzu yazın:", self.input_area)
        input_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        input_label.setGeometry(20, 15, 250, 30)
        input_label.setStyleSheet("color: white; background: transparent;")
        
        # Text input
        self.yazi_kutusu = QTextEdit(self.input_area)
        self.yazi_kutusu.setGeometry(20, 50, 1000, 120)
        self.yazi_kutusu.setPlaceholderText("Bugün hangi ürünü arıyorsunuz? Detaylı sorularınızı buraya yazabilirsiniz...")
        self.yazi_kutusu.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px;
                font-size: 18px;
                font-family: 'Segoe UI';
                selection-background-color: rgba(99, 102, 241, 0.5);
            }
            QTextEdit:focus {
                border: 2px solid rgba(99, 102, 241, 0.8);
                background: rgba(255, 255, 255, 0.15);
                box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
            }
        """)
        
        # Send button
        self.mesaj_butonu = ModernButton("🚀 Gönder", self.input_area)
        self.mesaj_butonu.setGeometry(1040, 60, 280, 100)
        self.mesaj_butonu.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.mesaj_butonu.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #10b981, stop:1 #059669);
                color: white;
                border: none;
                border-radius: 15px;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                box-shadow: 0 8px 32px rgba(16, 185, 129, 0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #059669, stop:1 #047857);
                box-shadow: 0 12px 40px rgba(16, 185, 129, 0.5);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                          stop:0 #047857, stop:1 #065f46);
                transform: translateY(0px);
            }
        """)
        self.mesaj_butonu.clicked.connect(self.sendMessage)
        
        # Chat display area
        self.sonuc_kutusu = QTextEdit(self.chat_container)
        self.sonuc_kutusu.setGeometry(20, 240, 1340, 490)
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.05);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 20px;
                font-size: 18px;
                font-family: 'Segoe UI';
                line-height: 1.6;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(99, 102, 241, 0.6);
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(99, 102, 241, 0.8);
            }
        """)

    def setup_animations(self):
        # Title entrance animation
        self.title_animation = QPropertyAnimation(self.title_label, b"pos")
        self.title_animation.setDuration(1000)
        self.title_animation.setEasingCurve(QEasingCurve.OutBounce)
        
        start_pos = QPoint(400, -50)
        end_pos = QPoint(400, 30)
        self.title_animation.setStartValue(start_pos)
        self.title_animation.setEndValue(end_pos)
        self.title_animation.start()
        
        # Panel slide animation
        self.panel_animation = QPropertyAnimation(self.left_panel, b"pos")
        self.panel_animation.setDuration(800)
        self.panel_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        panel_start = QPoint(-350, 100)
        panel_end = QPoint(30, 100)
        self.panel_animation.setStartValue(panel_start)
        self.panel_animation.setEndValue(panel_end)
        self.panel_animation.start()

    def sendMessage(self):
        kullanici_girdisi = self.yazi_kutusu.toPlainText().strip()
        if not kullanici_girdisi:
            return

        # Gemini API
        if not hasattr(self, 'model'):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel("models/gemini-2.0-flash")
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Gemini API hatası: {str(e)}")
                return

        # Ürün verilerini formatla
        urun_verisi = ""
        for urun in self.urunler:
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
           - **ÜRÜN:** Marka Model (Fiyat)
           - **NEDEN:** bu ürün? (kişisel özelliklerine uygunluk)
           - **AVANTAJLAR:** artı yönleri
           - **DİKKAT:** eksi yönleri
        3. Final önerisi ve nedeni
        4. Ek sorular (gerekirse)
        

        ⚡ KURALLAR:
        - Samimi ve profesyonel ol
        - Sadece mevcut ürünlerden öner
        - Bütçe '-' ise bütçe sor
        - Marka 'Farketmez' ise marka sorma
        - Çok detaya girme, net ol
        - Emojiler kullan ama abartma
        - Eğer kullanıcı bir ürünü almaya karar verirse kısa ve samimi bir dille doğru kararı verdiğini söyle
        - Ürün adlarını **ÜRÜN:** ile başlat ki grafik sistemi bulabilsin
        """

        if self.chat is None:
            self.chat = self.model.start_chat(history=[])
        
        cevap = self.chat.send_message(prompt)
        self.sohbeti_kaydet(kullanici_girdisi, cevap.text)

        # Önerilen ürünleri çıkar
        self.son_onerilen_urunler = self.urun_adlarini_cikart(cevap.text)
        
        # Grafik butonunu aktif et
        if self.son_onerilen_urunler:
            self.grafik_butonu.setEnabled(True)
            self.grafik_butonu.setText(f"📊 Grafik Göster ({len(self.son_onerilen_urunler)} ürün)")
        else:
            self.grafik_butonu.setEnabled(False)
            self.grafik_butonu.setText("📊 Grafik Göster")

        # Kullanıcı mesajı hemen gösterilir
        self.konusma_gecmisi.append(f"<div style='background: rgba(99, 102, 241, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #60a5fa;'>🧑 Siz:</span></b><br>{kullanici_girdisi}</div>")
        self.konusma_gecmisi.append(f"<div style='background: rgba(16, 185, 129, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #34d399;'>🤖 AI Asistan:</span></b><br>")
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

        # Typing efekt verisi
        formatli_cevap = self.ai_cevabini_formatla(cevap.text)
        self.typing_text = formatli_cevap

        self.typing_index = 0
        self.typing_timer.start(15)

        self.yazi_kutusu.clear()

    def urun_adlarini_cikart(self, ai_cevabi):
        """AI cevabından ürün adlarını çıkarır"""
        urun_listesi = []
        
        # **ÜRÜN:** ile başlayan satırları bul
        urun_pattern = r'\*\*ÜRÜN:\*\*\s*([^(]+)'
        urun_eslesmeleri = re.findall(urun_pattern, ai_cevabi)
        
        for urun in urun_eslesmeleri:
            temiz_urun = urun.strip()
            if temiz_urun:
                urun_listesi.append(temiz_urun)
        
        # Eğer **ÜRÜN:** formatı yoksa, genel ürün adı arama
        if not urun_listesi:
            for urun in self.urunler:
                urun_turu, marka, model, fiyat = urun
                tam_ad = f"{marka} {model}"
                if tam_ad.lower() in ai_cevabi.lower():
                    urun_listesi.append(tam_ad)
        
        return list(set(urun_listesi))

    def grafik_goster(self):
        """Önerilen ürünler için grafik pencerelerini aç"""
        if not self.son_onerilen_urunler:
            self.show_modern_message("Bilgi", "Önce bir ürün önerisi alın! 🛍️", "info")
            return
        
        try:
            for urun_adi in self.son_onerilen_urunler:
                grafik_penceresi = urun_grafik_goster(urun_adi, self)
                self.grafik_pencereleri.append(grafik_penceresi)
            
            self.show_modern_message("Başarılı", 
                                  f"✨ {len(self.son_onerilen_urunler)} ürün için grafik pencereleri açıldı!", "success")
            
        except ImportError:
            self.show_modern_message("Hata", 
                              "📊 Grafik modülü yüklenemiyor! matplotlib yüklü olduğundan emin olun.", "error")
        except Exception as e:
            self.show_modern_message("Hata", f"📊 Grafik gösterilirken hata oluştu: {str(e)}", "error")

    def show_modern_message(self, title, message, msg_type):
        """Modern mesaj kutusu göster"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
            style = """
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #d1fae5, stop:1 #a7f3d0);
                    color: #065f46;
                    border: 2px solid #34d399;
                    border-radius: 15px;
                    font-family: 'Segoe UI';
                }
                QMessageBox QLabel {
                    color: #065f46;
                    font-size: 14px;
                    padding: 10px;
                }
                QMessageBox QPushButton {
                    background: #10b981;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: #059669;
                }
            """
        elif msg_type == "info":
            msg_box.setIcon(QMessageBox.Information)
            style = """
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #dbeafe, stop:1 #bfdbfe);
                    color: #1e40af;
                    border: 2px solid #60a5fa;
                    border-radius: 15px;
                    font-family: 'Segoe UI';
                }
                QMessageBox QLabel {
                    color: #1e40af;
                    font-size: 14px;
                    padding: 10px;
                }
                QMessageBox QPushButton {
                    background: #3b82f6;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: #2563eb;
                }
            """
        else:  # error
            msg_box.setIcon(QMessageBox.Critical)
            style = """
                QMessageBox {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                              stop:0 #fee2e2, stop:1 #fecaca);
                    color: #991b1b;
                    border: 2px solid #f87171;
                    border-radius: 15px;
                    font-family: 'Segoe UI';
                }
                QMessageBox QLabel {
                    color: #991b1b;
                    font-size: 14px;
                    padding: 10px;
                }
                QMessageBox QPushButton {
                    background: #ef4444;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 8px;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background: #dc2626;
                }
            """
        
        msg_box.setStyleSheet(style)
        msg_box.exec_()
    
    def onceki_onerileri_goster(self):
        import os

        email = degiskenler.giris_yapan_email
        dosya_yolu = f"gecmisler/{email}.txt"
        
        if not os.path.exists(dosya_yolu):
            self.konusma_gecmisi.append("<div style='background: rgba(251, 191, 36, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0; text-align: center;'><b>📝 Daha önceki önerilere ulaşılamadı.</b></div>")
            self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))
            return

        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()

        oneriler = []
        for i, satir in enumerate(satirlar):
            if satir.startswith("    *   **ÜRÜN:**") or satir.startswith("*   **ÜRÜN:**") or satir.startswith("1.  **ÜRÜN:**") or satir.startswith("2.  **ÜRÜN:**"):
                oneriler.append(satirlar[i].strip())

        if oneriler:
            oneri_html = "<div style='background: rgba(168, 85, 247, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0;'>"
            oneri_html += "<h3 style='color: #a855f7; margin-bottom: 15px;'>📋 Önceki Ürün Önerileriniz</h3>"
            for i, oneri in enumerate(oneriler[:10], 1):  # Son 10 öneri
                oneri_html += f"<div style='margin: 8px 0; padding: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 8px;'>{i}. {oneri}</div>"
            oneri_html += "</div>"
        else:
            oneri_html = "<div style='background: rgba(156, 163, 175, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0; text-align: center;'><b>🤖 Daha önce size özel bir ürün önerisi sunulmamış.</b></div>"
        
        self.konusma_gecmisi.append(oneri_html)
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

    def urun_degistir(self, secilen_urun):
        self.marka_kutusu.clear()
        self.kullanim_kutusu.clear()

        self.marka_kutusu.addItems(degiskenler.marka_listeleri.get(secilen_urun, []))
        self.kullanim_kutusu.addItems(degiskenler.kullanim_amaci_listeleri.get(secilen_urun, []))

    def sohbeti_kaydet(self, kullanici_girdi, asistan_cevabi):
        dosya_adi = f"gecmisler/{degiskenler.giris_yapan_email}.txt"
        os.makedirs("gecmisler", exist_ok=True)
        with open(dosya_adi, "a", encoding="utf-8") as f:
            f.write(f"Kullanıcı: {kullanici_girdi}\n")
            f.write(f"Asistan: {asistan_cevabi}\n\n")

    def ai_cevabini_formatla(self, metin):
        """AI'dan gelen metni modern HTML formatına çevirir"""
        
        # Başlık kalıpları
        baslik_kaliplari = [
            "**Öneriler:**",
            "**ÜRÜN:**",
            "**NEDEN:**", 
            "**AVANTAJLAR:**",
            "**DİKKAT:**",
            "**Final Önerisi:**",
            "**Avantajları:**",
            "**Dezavantajları:**"
        ]
        
        # Başlıkları modern HTML'e çevir
        for kalip in baslik_kaliplari:
            temiz_baslik = kalip.replace("**", "").replace("*", "")
            if "ÜRÜN:" in kalip:
                html_baslik = f"<h3 style='color: #60a5fa; margin: 15px 0 10px 0; font-size: 16px;'>🛍️ {temiz_baslik}</h3>"
            elif "NEDEN:" in kalip:
                html_baslik = f"<h4 style='color: #34d399; margin: 10px 0 5px 0; font-size: 14px;'>💡 {temiz_baslik}</h4>"
            elif "AVANTAJLAR:" in kalip:
                html_baslik = f"<h4 style='color: #10b981; margin: 10px 0 5px 0; font-size: 14px;'>✅ {temiz_baslik}</h4>"
            elif "DİKKAT:" in kalip:
                html_baslik = f"<h4 style='color: #f59e0b; margin: 10px 0 5px 0; font-size: 14px;'>⚠️ {temiz_baslik}</h4>"
            else:
                html_baslik = f"<h3 style='color: #a855f7; margin: 15px 0 10px 0; font-size: 16px;'>✨ {temiz_baslik}</h3>"
            
            metin = metin.replace(kalip, html_baslik)
        
        # Ürün isimlerini vurgula
        import re
        metin = re.sub(r'(\d+\.)\s+([A-Za-zÇĞIİÖŞÜçğıiöşü\s\d\-]+(?:\([^)]*\))?)', 
                      r'<div style="background: rgba(99, 102, 241, 0.1); padding: 10px; border-radius: 10px; margin: 8px 0;"><b style="color: #8b5cf6;">\1 \2</b></div>', metin)
        
        # Diğer ** kalın yazıları HTML bold'a çevir
        metin = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', metin)
        
        return metin

    def sohbet_gecmisini_temizle(self):
        self.konusma_gecmisi.clear()
        self.sonuc_kutusu.clear()
        self.son_onerilen_urunler.clear()
        self.grafik_butonu.setEnabled(False)
        self.grafik_butonu.setText("📊 Grafik Göster")
        
        # Temizleme animasyonu
        self.konusma_gecmisi.append("<div style='background: rgba(34, 197, 94, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0; text-align: center;'><h3 style='color: #22c55e;'>✨ Sohbet temizlendi! Yeni bir konuşma başlayabilirsiniz.</h3></div>")
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

    def mod_degistir(self):
        self.gece_modu = not self.gece_modu
        
        if self.gece_modu:
            self.mod_butonu.setText("☀️ Gündüz")
            self.apply_dark_theme()
        else:
            self.mod_butonu.setText("🌙 Gece")
            self.apply_light_theme()

    def apply_dark_theme(self):
        # Gece modu renk paleti
        palet = QPalette()
        palet.setColor(QPalette.Window, QColor(15, 23, 42))
        palet.setColor(QPalette.WindowText, Qt.white)
        palet.setColor(QPalette.Base, QColor(30, 41, 59))
        palet.setColor(QPalette.Text, Qt.white)
        QApplication.setPalette(palet)
        
        # Karanlık tema stilleri
        dark_card_style = """
            QFrame {
                background: rgba(30, 41, 59, 0.8);
                border: 2px solid rgba(100, 116, 139, 0.3);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """
        self.left_panel.setStyleSheet(dark_card_style)
        self.chat_container.setStyleSheet(dark_card_style)

    def apply_light_theme(self):
        # Gündüz modu renk paleti
        QApplication.setPalette(QApplication.style().standardPalette())
        
        # Aydınlık tema stilleri
        light_card_style = """
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """
        self.left_panel.setStyleSheet(light_card_style)
        self.chat_container.setStyleSheet(light_card_style)
           
    def typeNextChar(self):
        if self.typing_index < len(self.typing_text):
            metin = self.typing_text[:self.typing_index + 1]
            full_html = "".join(self.konusma_gecmisi[:-1]) + f"<div style='background: rgba(16, 185, 129, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #34d399;'>🤖 AI Asistan:</span></b><br>{metin}</div>"
            self.sonuc_kutusu.setHtml(full_html)
            
            # Otomatik scroll
            scrollbar = self.sonuc_kutusu.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
            self.typing_index += 1
        else:
            self.konusma_gecmisi[-1] += f"{self.typing_text}</div>"
            self.typing_timer.stop()

    def cikis_yap(self):
        """Çıkış Yap butonu - giriş ekranına dön"""
        for pencere in self.grafik_pencereleri:
            if pencere:
                pencere.close()
        
        reply = QMessageBox.question(self, "🚪 Çıkış Yap", 
                                   "Giriş ekranına dönmek istiyor musunuz?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            from girisEkrani import LoginRegisterWindow
            self.login_window = LoginRegisterWindow()
            self.login_window.show()
            self.hide()

    def closeEvent(self, event):
        """Pencere kapatılırken açık grafik pencerelerini kapat"""
        for pencere in self.grafik_pencereleri:
            if pencere:
                pencere.close()
        QApplication.quit()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_start_position'):
            self.move(self.pos() + event.globalPos() - self.drag_start_position)
            self.drag_start_position = event.globalPos()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QIcon("robot.png"))
    
    chat_window = ChatWindow()
    chat_window.show()
    
    # Fade in animation
    fade_in = QPropertyAnimation(chat_window, b"windowOpacity")
    fade_in.setDuration(1000)
    fade_in.setStartValue(0.0)
    fade_in.setEndValue(1.0)
    fade_in.start()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()