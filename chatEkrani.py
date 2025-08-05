import threading
from functools import lru_cache
from urundeneme import urun_grafik_goster
from girisEkrani import *

# Urun verilerini import et
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
        self.setWindowIcon(QIcon("robot.png")) #<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Hilmy Abiyyu A. - Flaticon</a>
        
        # Modern pencere stili
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Performans optimizasyonlari
        self.ai_onbellegi = AICache(max_size=100)
        self.bellek_yoneticisi = MemoryManager(max_conversation_length=50)
        self.ai_isleyicisi = AsyncAIHandler(api_key, self.ai_onbellegi)
        self.yazma_zamanlayicisi = OptimizedTypingTimer()
        
        # AI handler baglantilar
        self.ai_isleyicisi.response_ready.connect(self.ai_cevabini_isle)
        self.ai_isleyicisi.error_occurred.connect(self.ai_hatasini_isle)
        
        # Yazma zamanlayici baglantilari
        self.yazma_zamanlayicisi.character_typed.connect(self.yazma_ekranini_guncelle)
        self.yazma_zamanlayicisi.typing_finished.connect(self.yazma_bittiginde)

        self.kullanici_email = degiskenler.giris_yapan_email
        self.konusma_gecmisi = []
        self.gece_modu = True
        self.urunler = tum_urunler
        self.son_onerilen_urunler = []
        self.grafik_pencereleri = []
        self.mevcut_ai_gelecegi = None
        
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

        self.arayuzu_baslat()
        self.animasyonlari_ayarla()
        
        # Bellek temizleme zamanlayicisi
        self.temizlik_zamanlayicisi = QTimer()
        self.temizlik_zamanlayicisi.timeout.connect(self.periyodik_temizlik)
        self.temizlik_zamanlayicisi.start(30000)  # 30 saniyede bir temizlik

    @lru_cache(maxsize=32)
    def urun_verilerini_formatlanmis_al(self):
        """Urun verilerini onbellekle"""
        urun_verisi = ""
        for urun in self.urunler:
            urun_turu, marka, model, fiyat, ozellikler = urun
            urun_verisi += f"{urun_turu} - Marka: {marka}, Model: {model}, Özellikler:{ozellikler}, Fiyat: {fiyat}\n"
        return urun_verisi

    def periyodik_temizlik(self):
        """Periyodik bellek temizligi"""
        # Konusma gecmisini yonet
        self.bellek_yoneticisi.manage_conversation(self.konusma_gecmisi)
        
        # Kapali grafik pencerelerini temizle
        self.grafik_pencereleri = self.bellek_yoneticisi.cleanup_graphics(self.grafik_pencereleri)
        
        # Onbellek boyutunu kontrol et
        if len(self.ai_onbellegi.cache) > 80:
            # Onbellegin %20'sini temizle
            silinecek_anahtarlar = list(self.ai_onbellegi.cache.keys())[:20]
            for anahtar in silinecek_anahtarlar:
                if anahtar in self.ai_onbellegi.cache:
                    del self.ai_onbellegi.cache[anahtar]
                if anahtar in self.ai_onbellegi.access_count:
                    del self.ai_onbellegi.access_count[anahtar]

    def arayuzu_baslat(self):
        # Ana konteyner
        self.ana_konteyner = QWidget(self)
        self.setCentralWidget(self.ana_konteyner)
        
        # Animasyonlu arkaplan
        self.arkaplan = AnimatedChatBackground(self)
        self.arkaplan.setGeometry(0, 0, 1800, 950)
        
        # Pencere kontrolleri
        self.pencere_kontrollerini_baslat()
        
        # Baslik bolumu
        self.basligi_baslat()
        
        # Sol panel (kontroller)
        self.sol_paneli_baslat()
        
        # Ana sohbet alani
        self.sohbet_alanini_baslat()

    def pencere_kontrollerini_baslat(self):
        # Kapatma butonu
        self.kapatma_butonu = QPushButton("✕", self)
        self.kapatma_butonu.setGeometry(1740, 20, 40, 40)
        self.kapatma_butonu.setStyleSheet("""
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
        self.kapatma_butonu.clicked.connect(self.close)
        
        # Kucultme butonu
        self.kucultme_butonu = QPushButton("—", self)
        self.kucultme_butonu.setGeometry(1690, 20, 40, 40)
        self.kucultme_butonu.setStyleSheet("""
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
        self.kucultme_butonu.clicked.connect(self.showMinimized)

    def basligi_baslat(self):
        # Baslik
        self.baslik_etiketi = QLabel("🤖 Premium AI Shopping Assistant", self)
        self.baslik_etiketi.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.baslik_etiketi.setAlignment(Qt.AlignCenter)
        self.baslik_etiketi.setGeometry(400, 30, 1000, 50)
        self.baslik_etiketi.setStyleSheet("""
            QLabel {
                color: white;
                background: transparent;
                text-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            }
        """)
        
        # Kullanici bilgisi
        self.kullanici_bilgisi = QLabel(f"👤 Hoş geldin, {self.kullanici_email}", self)
        self.kullanici_bilgisi.setFont(QFont("Segoe UI", 12))
        self.kullanici_bilgisi.setGeometry(50, 30, 300, 30)
        self.kullanici_bilgisi.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
        """)

    def sol_paneli_baslat(self):
        # Sol kontrol paneli
        self.sol_panel = GlassmorphismFrame(self)
        self.sol_panel.setGeometry(30, 100, 320, 800)
        self.sol_panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Panel basligi
        panel_basligi = QLabel("🎯 Arama Filtreleri", self.sol_panel)
        panel_basligi.setFont(QFont("Segoe UI", 16, QFont.Bold))
        panel_basligi.setGeometry(20, 20, 280, 40)
        panel_basligi.setStyleSheet("color: white; background: transparent; border: none; border-bottom: 2px solid rgba(255, 255, 255, 0.3);")
        
        # Urun turu
        self.urun_etiketi = QLabel("📱 Ürün Türü:", self.sol_panel)
        self.urun_etiketi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.urun_etiketi.setGeometry(20, 80, 280, 30)
        self.urun_etiketi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.urun_kutusu = QComboBox(self.sol_panel)
        self.urun_kutusu.addItems(degiskenler.urun_listesi)
        self.urun_kutusu.setGeometry(20, 115, 280, 50)
        self.urun_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        self.urun_kutusu.currentTextChanged.connect(self.urun_degistir)
        
        # Butce
        self.butce_etiketi = QLabel("💰 Bütçe Aralığı:", self.sol_panel)
        self.butce_etiketi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.butce_etiketi.setGeometry(20, 185, 280, 30)
        self.butce_etiketi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.butce_kutusu = QComboBox(self.sol_panel)
        self.butce_kutusu.addItems(degiskenler.butce_listesi)
        self.butce_kutusu.setGeometry(20, 220, 280, 50)
        self.butce_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Marka
        self.marka_etiketi = QLabel("🏷️ Marka Tercihi:", self.sol_panel)
        self.marka_etiketi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.marka_etiketi.setGeometry(20, 290, 280, 30)
        self.marka_etiketi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.marka_kutusu = QComboBox(self.sol_panel)
        self.marka_kutusu.addItems(degiskenler.tum_markalar)
        self.marka_kutusu.setGeometry(20, 325, 280, 50)
        self.marka_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Kullanim amaci
        self.kullanim_etiketi = QLabel("🎯 Kullanım Amacı:", self.sol_panel)
        self.kullanim_etiketi.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.kullanim_etiketi.setGeometry(20, 395, 280, 30)
        self.kullanim_etiketi.setStyleSheet("color: white; background: transparent; border: none;")
        
        self.kullanim_kutusu = QComboBox(self.sol_panel)
        self.kullanim_kutusu.addItems(degiskenler.tum_kullanim_amaclari)
        self.kullanim_kutusu.setGeometry(20, 430, 280, 50)
        self.kullanim_kutusu.setStyleSheet(degiskenler.modern_combobox_stili)
        
        # Eylem butonlari
        self.eylem_butonlarini_baslat()

    def eylem_butonlarini_baslat(self):
        # Onceki oneriler
        self.oneri_butonu = ModernButton("📋 Önceki Öneriler", self.sol_panel)
        self.oneri_butonu.setGeometry(20, 510, 280, 55)
        self.oneri_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.oneri_butonu.setStyleSheet(degiskenler.modern_buton_stili)
        self.oneri_butonu.clicked.connect(self.onceki_onerileri_goster)
        
        # Grafik butonu
        self.grafik_butonu = ModernButton("📊 Grafik Göster", self.sol_panel)
        self.grafik_butonu.setGeometry(20, 580, 280, 55)
        self.grafik_butonu.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.grafik_butonu.setStyleSheet(degiskenler.modern_buton_stili_2)
        self.grafik_butonu.clicked.connect(self.grafik_goster)
        self.grafik_butonu.setEnabled(False)
        
        # Sohbet temizleme
        self.temizleme_butonu = ModernButton("🗑️ Sohbeti Temizle", self.sol_panel)
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
        
        # Mod degistirme
        self.mod_butonu = ModernButton("☀️ Gündüz", self.sol_panel)
        self.mod_butonu.setGeometry(20, 720, 135, 55)
        self.mod_butonu.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.mod_butonu.setStyleSheet(degiskenler.mode_button_style)
        self.mod_butonu.clicked.connect(self.mod_degistir)
        
        # Cikis
        self.cikis_butonu = ModernButton("🚪 Çıkış", self.sol_panel)
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

    def sohbet_alanini_baslat(self):
        # Sohbet konteyneri
        self.sohbet_konteyneri = GlassmorphismFrame(self)
        self.sohbet_konteyneri.setGeometry(380, 100, 1380, 800)
        self.sohbet_konteyneri.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                backdrop-filter: blur(20px);
            }
        """)
        
        # Girdi alani
        self.girdi_alani = GlassmorphismFrame(self.sohbet_konteyneri)
        self.girdi_alani.setGeometry(20, 20, 1340, 200)
        self.girdi_alani.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border: 2px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
            }
        """)
        
        # Girdi etiketi
        girdi_etiketi = QLabel("💬 Sorununuzu yazın:", self.girdi_alani)
        girdi_etiketi.setFont(QFont("Segoe UI", 14, QFont.Bold))
        girdi_etiketi.setGeometry(20, 15, 250, 30)
        girdi_etiketi.setStyleSheet("color: white; background: transparent; border: none;")
        
        # Metin girdisi
        self.yazi_kutusu = QTextEdit(self.girdi_alani)
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
        
        # Gonderme butonu
        self.mesaj_butonu = ModernButton("🚀 Gönder", self.girdi_alani)
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
        self.mesaj_butonu.clicked.connect(self.mesaj_gonder)
        
        # Sohbet gosterim alani
        self.sonuc_kutusu = QTextEdit(self.sohbet_konteyneri)
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

    def animasyonlari_ayarla(self):
        # Baslik giris animasyonu
        self.baslik_animasyonu = QPropertyAnimation(self.baslik_etiketi, b"pos")
        self.baslik_animasyonu.setDuration(1000)
        self.baslik_animasyonu.setEasingCurve(QEasingCurve.OutBounce)
        
        baslangic_pozisyonu = QPoint(400, -50)
        bitis_pozisyonu = QPoint(400, 30)
        self.baslik_animasyonu.setStartValue(baslangic_pozisyonu)
        self.baslik_animasyonu.setEndValue(bitis_pozisyonu)
        self.baslik_animasyonu.start()
        
        # Panel kayma animasyonu
        self.panel_animasyonu = QPropertyAnimation(self.sol_panel, b"pos")
        self.panel_animasyonu.setDuration(800)
        self.panel_animasyonu.setEasingCurve(QEasingCurve.OutCubic)
        
        panel_baslangici = QPoint(-350, 100)
        panel_bitisi = QPoint(30, 100)
        self.panel_animasyonu.setStartValue(panel_baslangici)
        self.panel_animasyonu.setEndValue(panel_bitisi)
        self.panel_animasyonu.start()

    def mevcut_filtreleri_al(self):
        """Mevcut filtreleri dict olarak dondur"""
        return {
            'urun': self.urun_kutusu.currentText(),
            'butce': self.butce_kutusu.currentText(),
            'marka': self.marka_kutusu.currentText(),
            'kullanim': self.kullanim_kutusu.currentText()
        }

    def mesaj_gonder(self):
        from langdetect import detect
        kullanici_girdisi = self.yazi_kutusu.toPlainText().strip()
        if not kullanici_girdisi:
            return

        # Eger onceki bir AI istegi varsa iptal et
        if self.mevcut_ai_gelecegi and not self.mevcut_ai_gelecegi.done():
            self.mevcut_ai_gelecegi.cancel()

        # Send butonunu gecici olarak deaktif et
        self.mesaj_butonu.setEnabled(False)
        self.mesaj_butonu.setText("⏳ İşleniyor...")

        # Onbellek anahtari olustur
        mevcut_filtreler = self.mevcut_filtreleri_al()
        onbellek_anahtari = self.ai_onbellegi.get_cache_key(kullanici_girdisi, mevcut_filtreler)

        # Urun verilerini onbellekten al
        urun_verisi = self.urun_verilerini_formatlanmis_al()

        dil = detect(kullanici_girdisi)
        yanit_dili = "Türkçe" if dil == "tr" else "İngilizce"

        komut = f"""
        Sen uzman bir alışveriş danışmanısın. Kullanıcıya kişiselleştirilmiş ürün önerileri sunacaksın.

        🗣️ YANIT DİLİ: {yanit_dili}(yanıtını burdaki dile göre ver)

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
        - Aranan Ürün: {mevcut_filtreler['urun']}
        - Kullanım Amacı: {mevcut_filtreler['kullanim']}
        - Bütçe: {mevcut_filtreler['butce']}
        - Marka Tercihi: {mevcut_filtreler['marka']}

        💬 KULLANICI MESAJI: "{kullanici_girdisi}"(Bu kısım hangi dilde olursa sen de ona göre cevap ver lütfen)

        📝 CEVAP FORMATI:
        1. Kısa selamlama ve ihtiyaç özetı
        2. En uygun 2-3 ürün önerisi (her biri için):
           - **ÜRÜN:** Marka Model (Fiyat)
           - **NEDEN:** bu ürün? (kişisel özelliklerine uygunluk ve genel ürün özellikleri)
           - **AVANTAJLAR:** artı yönleri
           - **DİKKAT:** eksi yönleri
        3. Final önerisi ve nedeni
        4. Ek sorular (gerekirse)
        

        ⚡ KURALLAR:
        - Samimi ve profesyonel ol
        - Sadece mevcut ürünlerden öner
        - Bütçe '-' ise önce 2 tane ürün öner sonra bütçe sor
        - Marka 'Farketmez' ise marka sorma
        - Çok detaya girme, net ol
        - Emojiler kullan ama abartma
        - Eğer kullanıcı bir ürünü almaya karar verirse kısa ve samimi bir dille doğru kararı verdiğini söyle
        - Ürün adlarını **ÜRÜN:** ile başlat ki grafik sistemi bulabilsin
        """

        # Kullanici mesajini hemen goster
        self.konusma_gecmisi.append(f"<div style='background: rgba(99, 102, 241, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #60a5fa;'>🧑 Siz:</span></b><br>{kullanici_girdisi}</div>")
        self.konusma_gecmisi.append(f"<div style='background: rgba(16, 185, 129, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #34d399;'>🤖 AI Asistan:</span></b><br>")
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

        # Async AI islemini baslat
        self.mevcut_ai_gelecegi = self.ai_isleyicisi.send_message_async(komut, kullanici_girdisi, onbellek_anahtari)

        self.yazi_kutusu.clear()

    def ai_cevabini_isle(self, kullanici_girdisi, ai_cevabi):
        """AI yanitini isle"""
        # Sohbeti kaydet
        self.sohbeti_kaydet(kullanici_girdisi, ai_cevabi)

        # Onerilen urunleri cikar
        self.son_onerilen_urunler = self.urun_adlarini_cikart(ai_cevabi)
        
        # Grafik butonunu aktif et
        if self.son_onerilen_urunler:
            self.grafik_butonu.setEnabled(True)
            self.grafik_butonu.setText(f"📊 Grafik Göster ({len(self.son_onerilen_urunler)} ürün)")
        else:
            self.grafik_butonu.setEnabled(False)
            self.grafik_butonu.setText("📊 Grafik Göster")

        # Yazma efektini baslat
        formatli_cevap = self.ai_cevabini_formatla(ai_cevabi)
        self.yazma_zamanlayicisi.start_typing(formatli_cevap, speed=10)

        # Send butonunu tekrar aktif et
        self.mesaj_butonu.setEnabled(True)
        self.mesaj_butonu.setText("🚀 Gönder")

    def ai_hatasini_isle(self, hata_mesaji):
        """AI hatasini isle"""
        hata_html = f"<div style='background: rgba(239, 68, 68, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0; text-align: center;'><b style='color: #f87171;'>❌ Hata: {hata_mesaji}</b></div>"
        self.konusma_gecmisi.append(hata_html)
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))
        
        # Send butonunu tekrar aktif et
        self.mesaj_butonu.setEnabled(True)
        self.mesaj_butonu.setText("🚀 Gönder")

    def yazma_ekranini_guncelle(self, mevcut_metin):
        """Yazma efekti sirasinda ekrani guncelle"""
        tam_html = "".join(self.konusma_gecmisi[:-1]) + f"<div style='background: rgba(16, 185, 129, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0;'><b><span style='color: #34d399;'>🤖 AI Asistan:</span></b><br>{mevcut_metin}</div>"
        self.sonuc_kutusu.setHtml(tam_html)
        
        # Otomatik kaydirma
        kaydirma_cubugu = self.sonuc_kutusu.verticalScrollBar()
        kaydirma_cubugu.setValue(kaydirma_cubugu.maximum())

    def yazma_bittiginde(self):
        """Yazma efekti bittiginde"""
        # Son HTML'i konusma gecmisine ekle
        if self.konusma_gecmisi:
            self.konusma_gecmisi[-1] += f"{self.yazma_zamanlayicisi.typing_text}</div>"

    @lru_cache(maxsize=16)
    def urun_adlarini_cikart(self, ai_cevabi):
        from re import findall
        """AI cevabindan urun adlarini cikarir - onbellekli"""
        urun_listesi = []
        
        # **ÜRÜN:** ile baslayan satirlari bul
        urun_deseni = r'\*\*ÜRÜN:\*\*\s*([^(]+)'
        urun_eslesmeler = findall(urun_deseni, ai_cevabi)
        
        for urun in urun_eslesmeler:
            temiz_urun = urun.strip()
            if temiz_urun:
                urun_listesi.append(temiz_urun)
        
        # Eger **ÜRÜN:** formati yoksa, genel urun adi arama
        if not urun_listesi:
            for urun in self.urunler:
                urun_turu, marka, model, fiyat, ozellikler = urun
                tam_ad = f"{marka} {model}"
                if tam_ad.lower() in ai_cevabi.lower():
                    urun_listesi.append(tam_ad)
        
        return list(set(urun_listesi))  # tuple for hashability

    def grafik_goster(self):
        """Onerilen urunler icin grafik pencerelerini ac"""
        if not self.son_onerilen_urunler:
            QMessageBox.information(self, "Bilgi", "Önce bir ürün önerisi alın!")
            return
        
        try:
            # Her onerilen urun icin grafik penceresi ac
            for urun_adi in self.son_onerilen_urunler:
                grafik_penceresi = urun_grafik_goster(urun_adi, self)
                self.grafik_pencereleri.append(grafik_penceresi)
            
            # Basari mesaji
            QMessageBox.information(self, "Başarılı", 
                                  f"{len(self.son_onerilen_urunler)} ürün için grafik pencereleri açıldı!")
            
        except ImportError:
            QMessageBox.warning(self, "Hata", 
                              "Grafik modülü yüklenemiyor! matplotlib yüklü olduğundan emin olun.")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Grafik gösterilirken hata oluştu: {str(e)}")

    def grafik_acildi(self, yeni_pencereler):
        """Grafik pencereleri basariyla acildiginda"""
        self.grafik_pencereleri.extend(yeni_pencereler)
        self.modern_mesaj_goster("Başarılı", 
                              f"✨ {len(self.son_onerilen_urunler)} ürün için grafik pencereleri açıldı!", "success")
        
        # Butonu tekrar aktif et
        self.grafik_butonu.setEnabled(True)
        self.grafik_butonu.setText(f"📊 Grafik Göster ({len(self.son_onerilen_urunler)} ürün)")

    def grafik_hatasi(self, hata_mesaji):
        """Grafik hatasi durumunda"""
        if "ImportError" in hata_mesaji or "matplotlib" in hata_mesaji:
            self.modern_mesaj_goster("Hata", 
                              "📊 Grafik modülü yüklenemiyor! matplotlib yüklü olduğundan emin olun.", "error")
        else:
            self.modern_mesaj_goster("Hata", f"📊 Grafik gösterilirken hata oluştu: {hata_mesaji}", "error")
        
        # Butonu tekrar aktif et
        self.grafik_butonu.setEnabled(True)
        self.grafik_butonu.setText(f"📊 Grafik Göster ({len(self.son_onerilen_urunler)} ürün)")

    def modern_mesaj_goster(self, baslik, mesaj, mesaj_turu):
        """Modern mesaj kutusu goster"""
        mesaj_kutusu = QMessageBox(self)
        mesaj_kutusu.setWindowTitle(baslik)
        mesaj_kutusu.setText(mesaj)
        
        if mesaj_turu == "success":
            mesaj_kutusu.setIcon(QMessageBox.Information)
            stil = """
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
        elif mesaj_turu == "info":
            mesaj_kutusu.setIcon(QMessageBox.Information)
            stil = """
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
            mesaj_kutusu.setIcon(QMessageBox.Critical)
            stil = """
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
        
        mesaj_kutusu.setStyleSheet(stil)
        mesaj_kutusu.exec_()
    
    def onceki_onerileri_goster(self):
        """Onceki onerileri goster - optimize edilmis"""
        self.sonuc_kutusu.clear()
        def onerileri_yukle():
            """Onerileri arka planda yukle"""
            try:
                email = degiskenler.giris_yapan_email
                dosya_yolu = f"gecmisler/{email}.txt"
                
                if not os.path.exists(dosya_yolu):
                    return None, "Daha önceki önerilere ulaşılamadı."

                with open(dosya_yolu, "r", encoding="utf-8") as dosya:
                    satirlar = dosya.readlines()

                oneriler = []
                for i, satir in enumerate(satirlar):
                    if satir.startswith("   - **ÜRÜN") or satir.startswith("   - **PRODUCT") or satir.startswith("2.  **ÜRÜN")or satir.startswith("1.  **ÜRÜN") or satir.startswith("*   **ÜRÜN") or satir.startswith("- **ÜRÜN") or satir.startswith("- **PRODUCT") or satir.startswith("*   **PRODUCT"):
                        oneriler.append(satirlar[i].strip()) 

                if oneriler:
                    mesaj = "İşte önceki bazı ürün önerilerin:\n\n" + "\n".join(f"• {o}" for o in oneriler[:])  # Son 5 tanesi
                else:
                    mesaj = "Daha önce sana özel bir ürün önerisi sunulmamış."
                self.sonuc_kutusu.append(mesaj)
                return oneriler
            except:
                self.sonuc_kutusu.append("Bir hata oluştu")     

        # Arka planda yukle
        def onerileri_isle():
            oneriler = onerileri_yukle()
            QTimer.singleShot(0, lambda: self.onerileri_goster(oneriler))

        threading.Thread(target=onerileri_isle, daemon=True).start()

    def onerileri_goster(self, oneriler):
        """Onerileri ana thread'de goster"""
        if oneriler:
            oneri_html = "<div style='background: rgba(168, 85, 247, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0;'>"
            oneri_html += "<h3 style='color: #a855f7; margin-bottom: 15px;'>📋 Önceki Ürün Önerileriniz</h3>"
            for i, oneri in enumerate(oneriler[:10], 1):  # Son 10 oneri
                oneri_html += f"<div style='margin: 8px 0; padding: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 8px;'>{i}. {oneri}</div>"
            oneri_html += "</div>"
        else:
            oneri_html = "<div style='background: rgba(156, 163, 175, 0.2); padding: 15px; border-radius: 15px; margin: 10px 0; text-align: center;'><b>🤖 Daha önce size özel bir ürün önerisi sunulmamış.</b></div>"
        
        self.konusma_gecmisi.append(oneri_html)
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

    def urun_degistir(self, secilen_urun):
        """Urun degistiginde markalari ve kullanim amaclarini guncelle"""
        self.marka_kutusu.clear()
        self.kullanim_kutusu.clear()

        self.marka_kutusu.addItems(degiskenler.marka_listeleri.get(secilen_urun, []))
        self.kullanim_kutusu.addItems(degiskenler.kullanim_amaci_listeleri.get(secilen_urun, []))

    def sohbeti_kaydet(self, kullanici_girdi, asistan_cevabi):
        """Sohbeti arka planda kaydet"""
        def sohbet_kaydet():
            try:
                dosya_adi = f"gecmisler/{degiskenler.giris_yapan_email}.txt"
                os.makedirs("gecmisler", exist_ok=True)
                with open(dosya_adi, "a", encoding="utf-8") as f:
                    f.write(f"Kullanıcı: {kullanici_girdi}\n")
                    f.write(f"Asistan: {asistan_cevabi}\n\n")
            except Exception as e:
                print(f"Sohbet kaydetme hatası: {e}")

        threading.Thread(target=sohbet_kaydet, daemon=True).start()

    @lru_cache(maxsize=32)
    def ai_cevabini_formatla(self, metin):
        import re
        """AI'dan gelen metni modern HTML formatina cevirir - onbellekli"""
        
        # Baslik kaliplari
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
        
        # Basliklari modern HTML'e cevir
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
        
        # Urun isimlerini vurgula    
        metin = re.sub(r'(\d+\.)\s+([A-Za-zÇĞIİÖŞÜçğıiöşü\s\d\-]+(?:\([^)]*\))?)', 
                      r'<div style="background: rgba(99, 102, 241, 0.1); padding: 10px; border-radius: 10px; margin: 8px 0;"><b style="color: #8b5cf6;">\1 \2</b></div>', metin)
        
        # Diger ** kalin yazilari HTML bold'a cevir
        metin = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', metin)
        return metin

    def sohbet_gecmisini_temizle(self):
        """Sohbet geçmişini temizle - cache'leri de temizle"""
        self.konusma_gecmisi.clear()
        self.sonuc_kutusu.clear()
        self.son_onerilen_urunler.clear()
        self.grafik_butonu.setEnabled(False)
        self.grafik_butonu.setText("📊 Grafik Göster")
        
        # Cache'leri temizle
        self.ai_onbellegi.clear()
        self.ai_cevabini_formatla.cache_clear()
        self.urun_adlarini_cikart.cache_clear()
        
        # Temizleme animasyonu
        self.konusma_gecmisi.append("<div style='background: rgba(34, 197, 94, 0.2); padding: 20px; border-radius: 15px; margin: 10px 0; text-align: center;'><h3 style='color: #22c55e;'>✨ Sohbet temizlendi! Yeni bir konuşma başlayabilirsiniz.</h3></div>")
        self.sonuc_kutusu.setHtml("".join(self.konusma_gecmisi))

    def mod_degistir(self):
        """Gece/Gündüz modu değiştir"""
        self.gece_modu = not self.gece_modu
        if self.gece_modu:
            self.mod_butonu.setText("☀️ Gündüz")

            # Gece modu renk paleti
            palet = QPalette()
            palet.setColor(QPalette.Window, QColor(15, 23, 42))
            palet.setColor(QPalette.WindowText, Qt.white)
            palet.setColor(QPalette.Base, QColor(30, 41, 59))
            palet.setColor(QPalette.Text, Qt.white)
            QApplication.setPalette(palet)
            
            # Karanlık tema stilleri
            koyu_kart_stili = """
                QFrame {
                    background: rgba(30, 41, 59, 0.8);
                    border: 2px solid rgba(100, 116, 139, 0.3);
                    border-radius: 20px;
                    backdrop-filter: blur(20px);
                }
            """
            self.sol_panel.setStyleSheet(koyu_kart_stili)
            self.sohbet_konteyneri.setStyleSheet(koyu_kart_stili)
        else:
            self.mod_butonu.setText("🌙 Gece")
            """Gündüz modu tema uygula"""
            # Gündüz modu renk paleti
            QApplication.setPalette(QApplication.style().standardPalette())
            
            # Aydınlık tema stilleri
            acik_kart_stili = """
                QFrame {
                    background: rgba(255, 255, 255, 0.1);
                    border: 2px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px;
                    backdrop-filter: blur(20px);
                }
            """
            self.sol_panel.setStyleSheet(acik_kart_stili)
            self.sohbet_konteyneri.setStyleSheet(acik_kart_stili)   
       
    def cikis_yap(self):
        """Çıkış Yap butonu - giriş ekranına dön"""
        # Açık grafik pencerelerini kapat
        for pencere in self.grafik_pencereleri:
            if pencere:
                try:
                    pencere.close()
                except:
                    pass
        
        cevap = QMessageBox.question(self, "🚪 Çıkış Yap", 
                                   "Giriş ekranına dönmek istiyor musunuz?",
                                   QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            self.giris_ekrani = LoginWindow()
            self.giris_ekrani.show()
            self.hide()

    def closeEvent(self, event):
        """Pencere kapatılırken cleanup işlemleri"""
        try:
            # Timer'ları durdur
            self.temizlik_zamanlayicisi.stop()
            self.yazma_zamanlayicisi.stop_typing()
            
            # AI handler'ı temizle
            if hasattr(self.ai_isleyicisi, 'executor'):
                self.ai_isleyicisi.shutdown(wait=False)
            
            # Mevcut AI isteğini iptal et
            if self.mevcut_ai_gelecegi and not self.mevcut_ai_gelecegi.done():
                self.mevcut_ai_gelecegi.cancel()
            
            # Açık grafik pencerelerini kapat
            for pencere in self.grafik_pencereleri:
                if pencere:
                    try:
                        pencere.close()
                    except:
                        pass
            
            # Cache'leri temizle
            self.ai_onbellegi.clear()
            
            # Garbage collection
            gc.collect()
            
        except Exception as e:
            print(f"Cleanup hatası: {e}")
        
        QApplication.quit()
        event.accept()

    def fare_tiklamasi(self, event):
        """pencere taşıma için"""
        if event.button() == Qt.LeftButton:
            self.surukleme_pozisyonu = event.globalPos()

    def fare_suruklemesi(self, event):
        """pencere taşıma için"""
        if event.buttons() == Qt.LeftButton and hasattr(self, 'surukleme_pozisyonu'):
            self.move(self.pos() + event.globalPos() - self.surukleme_pozisyonu)
            self.surukleme_pozisyonu = event.globalPos()

def main():
    uygulama = QApplication(sys.argv)
    uygulama.setStyle('Fusion')
    uygulama.setWindowIcon(QIcon("robot.png")) #<a href="https://www.flaticon.com/free-icons/robot" title="robot icons">Robot icons created by Hilmy Abiyyu A. - Flaticon</a>
    
    uygulama_ekrani = LoginWindow()
    uygulama_ekrani.show()
    
    # Fade in animation
    kaybolma_animasyonu = QPropertyAnimation(uygulama_ekrani, b"windowOpacity")
    kaybolma_animasyonu.setDuration(1000)
    kaybolma_animasyonu.setStartValue(0.0)
    kaybolma_animasyonu.setEndValue(1.0)
    kaybolma_animasyonu.start()
    
    sys.exit(uygulama.exec_())

if __name__ == "__main__":
    main()