import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import datetime
import random
import numpy as np

# Ürün verilerini import et
try:
    from urunler import telefonlar, bilgisayarlar, kameralar, kulakliklar, tabletler
    
    # Tüm ürünleri birleştir
    tum_urunler = telefonlar + bilgisayarlar + kameralar + kulakliklar + tabletler
except ImportError:
    print("urunler.py dosyası bulunamadı!")
    tum_urunler = []

class GrafikPenceresi(QMainWindow):
    def __init__(self, urun_adi, parent=None):
        super().__init__(parent)
        self.urun_adi = urun_adi
        self.setWindowTitle(f"{urun_adi} - Fiyat Grafik Analizi")
        self.setGeometry(200, 200, 1200, 800)
        self.setWindowIcon(QIcon("robot.png"))
        
        self.initUI()
        self.grafik_olustur()

    def initUI(self):
        # Ana widget ve layout
        ana_widget = QWidget()
        self.setCentralWidget(ana_widget)
        layout = QVBoxLayout(ana_widget)

        # Başlık
        baslik = QLabel(f"📊 {self.urun_adi} Fiyat Analizi")
        baslik.setAlignment(Qt.AlignCenter)
        baslik.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
                margin: 10px;
            }
        """)
        layout.addWidget(baslik)

        # Grafik widget'ı
        self.grafik_widget = QWidget()
        layout.addWidget(self.grafik_widget)

        # Alt panel
        alt_panel = QWidget()
        alt_layout = QHBoxLayout(alt_panel)
        
        # Bilgi paneli
        self.bilgi_paneli = QTextEdit()
        self.bilgi_paneli.setMaximumHeight(150)
        self.bilgi_paneli.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        alt_layout.addWidget(self.bilgi_paneli)

        # Butonlar
        buton_paneli = QWidget()
        buton_layout = QVBoxLayout(buton_paneli)
        
        self.yenile_butonu = QPushButton("🔄 Yenile")
        self.yenile_butonu.clicked.connect(self.grafik_olustur)
        self.yenile_butonu.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        self.kapat_butonu = QPushButton("❌ Kapat")
        self.kapat_butonu.clicked.connect(self.close)
        self.kapat_butonu.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        buton_layout.addWidget(self.yenile_butonu)
        buton_layout.addWidget(self.kapat_butonu)
        buton_layout.addStretch()
        
        alt_layout.addWidget(buton_paneli)
        layout.addWidget(alt_panel)

    def urun_fiyat_verisi_olustur(self):
        """Ürünler.py dosyasından güncel fiyatı alıp, geçmiş 30 günlük mantıklı fiyat verisi oluşturur"""
        # Son 30 günlük veri
        bugun = datetime.datetime.now()
        tarihler = [bugun - datetime.timedelta(days=i) for i in range(30, 0, -1)]
        
        # Ürünler.py dosyasından ürün bilgisi al - güncel fiyat
        guncel_fiyat = None
        bulunan_urun = None
        
        print(f"\n🔍 Aranan ürün: '{self.urun_adi}'")
        print(f"📦 Toplam {len(tum_urunler)} ürün kontrol ediliyor...")
        
        # Akıllı ürün eşleştirme sistemi
        en_iyi_eslesme = None
        en_yuksek_skor = 0
        
        try:
            for urun in tum_urunler:
                urun_turu, marka, model, fiyat_str = urun
                tam_ad = f"{marka} {model}"
                
                # Eşleştirme skoru hesapla
                skor = self.urun_eslesme_skoru_hesapla(self.urun_adi, tam_ad, marka, model)
                
                print(f"🔎 Kontrol: '{tam_ad}' - Skor: {skor:.2f} - Fiyat: '{fiyat_str}'")
                
                if skor > en_yuksek_skor:
                    en_yuksek_skor = skor
                    en_iyi_eslesme = urun
                    print(f"   ⭐ Yeni en iyi eşleşme! Skor: {skor:.2f}")
            
            # En iyi eşleşmeyi kullan (minimum skor 0.3)
            if en_iyi_eslesme and en_yuksek_skor >= 0.3:
                urun_turu, marka, model, fiyat_str = en_iyi_eslesme
                tam_ad = f"{marka} {model}"
                guncel_fiyat = self.fiyat_parse_et(fiyat_str)
                bulunan_urun = tam_ad
                print(f"✅ En iyi eşleşen ürün: {tam_ad} (Skor: {en_yuksek_skor:.2f})")
                print(f"💰 Fiyat: '{fiyat_str}' → Parse edilen: {guncel_fiyat} ₺")
            else:
                print(f"❌ Yeterli eşleşme bulunamadı. En yüksek skor: {en_yuksek_skor:.2f}")
                        
        except Exception as e:
            print(f"❌ Ürün arama hatası: {e}")

        # Eğer hiç ürün bulunamazsa varsayılan fiyat
        if guncel_fiyat is None or guncel_fiyat <= 0:
            guncel_fiyat = 15000.0  # Varsayılan fiyat
            print(f"⚠️ Ürün bulunamadı ({self.urun_adi}), varsayılan fiyat kullanılıyor: {guncel_fiyat} ₺")
        else:
            print(f"🎯 Final güncel fiyat: {guncel_fiyat} ₺ ({bulunan_urun})")

        # Geçmiş fiyatları güncel fiyattan geriye doğru mantıklı şekilde oluştur
        fiyatlar = []
        
        # Son fiyat güncel fiyat olacak
        fiyatlar.append(guncel_fiyat)
        
        # Geriye doğru fiyat geçmişi oluştur
        for i in range(1, 30):  # 29 gün geriye git
            tarih_index = 29 - i  # Geriye doğru
            tarih = tarihler[tarih_index]
            
            # Önceki günün fiyatını al
            onceki_fiyat = fiyatlar[0]
            
            # Fiyat değişim faktörleri
            # Hafta sonu promosyonları (Cuma-Cumartesi-Pazar)
            if tarih.weekday() in [4, 5, 6]:  # Cuma, Cumartesi, Pazar
                hafta_sonu_faktor = random.uniform(1.02, 1.08)  # %2-8 daha yüksek
            else:
                hafta_sonu_faktor = random.uniform(0.98, 1.02)
            
            # Genel trend (fiyatlar genelde zamanla düşer)
            trend_faktor = random.uniform(1.001, 1.003)  # Hafif yükselme trendi geriye giderken
            
            # Günlük dalgalanma
            gunluk_degisim = random.uniform(0.995, 1.005)  # %0.5 dalgalanma
            
            # Özel günler (ayın başı/sonu promosyonları)
            if tarih.day <= 3 or tarih.day >= 28:
                ozel_gun_faktor = random.uniform(1.01, 1.05)
            else:
                ozel_gun_faktor = 1.0
            
            # Yeni fiyatı hesapla
            yeni_fiyat = onceki_fiyat * hafta_sonu_faktor * trend_faktor * gunluk_degisim * ozel_gun_faktor
            
            # Makul sınırlar koy (güncel fiyatın %70-130'u arası)
            min_fiyat = guncel_fiyat * 0.70
            max_fiyat = guncel_fiyat * 1.30
            yeni_fiyat = max(min_fiyat, min(max_fiyat, yeni_fiyat))
            
            fiyatlar.insert(0, yeni_fiyat)  # Başa ekle
        
        return tarihler, fiyatlar

    def urun_eslesme_skoru_hesapla(self, aranan, tam_ad, marka, model):
        """Ürün adı eşleştirme skorunu hesaplar (0-1 arası)"""
        skor = 0.0
        aranan_lower = aranan.lower().strip()
        tam_ad_lower = tam_ad.lower().strip()
        marka_lower = marka.lower().strip()
        model_lower = model.lower().strip()
        
        # 1. Tam eşleşme (en yüksek skor)
        if aranan_lower == tam_ad_lower:
            return 1.0
        
        # 2. Tam ürün adı aranan içinde geçiyor
        if tam_ad_lower in aranan_lower:
            skor += 0.8
        
        # 3. Aranan ürün adı tam ürün adı içinde geçiyor
        if aranan_lower in tam_ad_lower:
            skor += 0.6
        
        # 4. Marka eşleşmesi
        if marka_lower in aranan_lower:
            skor += 0.3
        
        # 5. Model eşleşmesi
        if model_lower in aranan_lower:
            skor += 0.4
        
        # 6. Kelime kelime eşleştirme
        aranan_kelimeler = aranan_lower.split()
        tam_ad_kelimeler = tam_ad_lower.split()
        
        eslesen_kelime_sayisi = 0
        for kelime in aranan_kelimeler:
            if len(kelime) > 2:  # Çok kısa kelimeleri sayma
                for tam_kelime in tam_ad_kelimeler:
                    if kelime in tam_kelime or tam_kelime in kelime:
                        eslesen_kelime_sayisi += 1
                        break
        
        if len(aranan_kelimeler) > 0:
            kelime_skoru = eslesen_kelime_sayisi / len(aranan_kelimeler)
            skor += kelime_skoru * 0.5
        
        # 7. Özel durumlar (sayılar, kısaltmalar)
        import re
        aranan_sayilar = re.findall(r'\d+', aranan)
        tam_ad_sayilar = re.findall(r'\d+', tam_ad)
        
        for sayi in aranan_sayilar:
            if sayi in tam_ad_sayilar:
                skor += 0.2
        
        # Maksimum 1.0 skor
        return min(skor, 1.0)

    def fiyat_parse_et(self, fiyat_str):
        """Fiyat string'ini doğru şekilde parse eder"""
        if not fiyat_str:
            return 0.0
        
        try:
            # String'i temizle
            temiz_fiyat = str(fiyat_str).strip()
            print(f"Temizlenecek fiyat: '{temiz_fiyat}'")
            
            # ₺ işaretini kaldır
            temiz_fiyat = temiz_fiyat.replace('₺', '').strip()
            
            # TL kelimesini kaldır
            temiz_fiyat = temiz_fiyat.replace('TL', '').replace('tl', '').strip()
            
            # Boşlukları kaldır
            temiz_fiyat = temiz_fiyat.replace(' ', '')
            
            print(f"₺ ve TL kaldırıldıktan sonra: '{temiz_fiyat}'")
            
            # Eğer nokta binlik ayırıcısı olarak kullanılıyorsa (8.500,50 gibi)
            if ',' in temiz_fiyat and '.' in temiz_fiyat:
                # Noktalar binlik ayırıcı, virgül ondalık ayırıcı
                temiz_fiyat = temiz_fiyat.replace('.', '').replace(',', '.')
            elif '.' in temiz_fiyat and temiz_fiyat.count('.') == 1:
                # Tek nokta var - kontrol et hangisi
                parts = temiz_fiyat.split('.')
                if len(parts[1]) <= 2:  # Ondalık kısım 2 hane veya daha az -> ondalık ayırıcı
                    pass  # Olduğu gibi bırak
                else:  # 3 hane veya daha fazla -> binlik ayırıcı
                    temiz_fiyat = temiz_fiyat.replace('.', '')
            elif ',' in temiz_fiyat and temiz_fiyat.count(',') == 1:
                # Tek virgül var - ondalık ayırıcı olarak değiştir
                temiz_fiyat = temiz_fiyat.replace(',', '.')
            elif '.' in temiz_fiyat and temiz_fiyat.count('.') > 1:
                # Birden fazla nokta -> hepsi binlik ayırıcı
                parts = temiz_fiyat.split('.')
                temiz_fiyat = ''.join(parts)
            
            print(f"Formatlandıktan sonra: '{temiz_fiyat}'")
            
            # Float'a çevir
            fiyat = float(temiz_fiyat)
            print(f"Parse edilen fiyat: {fiyat}")
            
            return fiyat
            
        except Exception as e:
            print(f"Fiyat parse hatası: {e}, Original: '{fiyat_str}'")
            return 0.0

    def grafik_olustur(self):
        # Mevcut grafik widget'ını temizle
        if hasattr(self, 'canvas'):
            self.canvas.setParent(None)

        # Veri oluştur
        tarihler, fiyatlar = self.urun_fiyat_verisi_olustur()

        # Matplotlib figure oluştur
        self.figure = Figure(figsize=(12, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        
        # Grafik widget'ına ekle
        if self.grafik_widget.layout():
            for i in reversed(range(self.grafik_widget.layout().count())): 
                self.grafik_widget.layout().itemAt(i).widget().setParent(None)
        else:
            self.grafik_widget.setLayout(QVBoxLayout())
        
        self.grafik_widget.layout().addWidget(self.canvas)

        # Ana grafik
        ax1 = self.figure.add_subplot(211)
        ax1.plot(tarihler, fiyatlar, 'b-', linewidth=2, label='Fiyat')
        ax1.fill_between(tarihler, fiyatlar, alpha=0.3, color='lightblue')
        
        # Trend çizgisi
        z = np.polyfit(range(len(fiyatlar)), fiyatlar, 1)
        trend_line = np.poly1d(z)
        ax1.plot(tarihler, trend_line(range(len(fiyatlar))), 'r--', linewidth=1, label='Trend')

        ax1.set_title(f'{self.urun_adi} - Son 30 Gün Fiyat Değişimi', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Fiyat (₺)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Tarih formatı
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        self.figure.autofmt_xdate()

        # Fiyat değişim yüzdesi grafiği
        ax2 = self.figure.add_subplot(212)
        degisim_yuzdesi = [(fiyatlar[i] - fiyatlar[0]) / fiyatlar[0] * 100 for i in range(len(fiyatlar))]
        
        renkler = ['red' if x < 0 else 'green' for x in degisim_yuzdesi]
        ax2.bar(tarihler, degisim_yuzdesi, color=renkler, alpha=0.6, width=0.8)
        ax2.set_title('Fiyat Değişim Yüzdesi (%)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Değişim (%)', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

        self.figure.tight_layout()
        self.canvas.draw()

        # İstatistik bilgilerini güncelle
        self.istatistik_guncelle(fiyatlar)

    def istatistik_guncelle(self, fiyatlar):
        """İstatistik bilgilerini günceller"""
        min_fiyat = min(fiyatlar)
        max_fiyat = max(fiyatlar)
        ort_fiyat = sum(fiyatlar) / len(fiyatlar)
        guncel_fiyat = fiyatlar[-1]  # Son fiyat (bugünkü) = veritabanındaki fiyat
        
        # Fiyat değişimi (30 gün öncesine göre)
        baslangic_fiyat = fiyatlar[0]  # 30 gün önceki fiyat
        fiyat_degisimi = guncel_fiyat - baslangic_fiyat
        degisim_yuzdesi = (fiyat_degisimi / baslangic_fiyat) * 100

        # En iyi satın alma günü
        en_dusuk_gun = fiyatlar.index(min_fiyat)
        
        # Tasarruf hesapla
        tasarruf_miktar = max_fiyat - guncel_fiyat
        tasarruf_yuzde = (tasarruf_miktar / max_fiyat) * 100 if max_fiyat > 0 else 0

        bilgi_metni = f"""
📈 <b>FİYAT ANALİZİ RAPORU</b>

💰 <b>Güncel Fiyat:</b> {guncel_fiyat:.2f} ₺ (Veritabanından)
📊 <b>30 Günlük Ortalama:</b> {ort_fiyat:.2f} ₺
📉 <b>En Düşük Fiyat:</b> {min_fiyat:.2f} ₺ ({30-en_dusuk_gun} gün önce)
📈 <b>En Yüksek Fiyat:</b> {max_fiyat:.2f} ₺

📅 <b>30 Günlük Değişim:</b> {fiyat_degisimi:.2f} ₺ ({degisim_yuzdesi:+.1f}%)

💡 <b>Fiyat Durumu:</b>
• Güncel fiyat ortalamanın {'altında' if guncel_fiyat < ort_fiyat else 'üstünde'} ({abs(guncel_fiyat - ort_fiyat):.2f} ₺)
• En yüksek fiyata göre {tasarruf_yuzde:.1f}% tasarruf ediyorsunuz

🎯 <b>Satın Alma Önerisi:</b>
• {'📈 Fiyatlar yükseliş trendinde - Almak için iyi zaman!' if degisim_yuzdesi > 0 else '📉 Fiyatlar düşüş trendinde - Biraz beklemek daha avantajlı olabilir'}
• {'🟢 Ortalamadan düşük - Uygun fiyat!' if guncel_fiyat < ort_fiyat else '🟡 Ortalamadan yüksek - Beklemek mantıklı'}

⚡ <b>Fiyat Aralığı:</b> {max_fiyat - min_fiyat:.2f} ₺ fark var (30 günde)
        """
        
        self.bilgi_paneli.setHtml(bilgi_metni)

def urun_grafik_goster(urun_adi, parent=None):
    """Ürün grafik penceresini aç"""
    grafik_penceresi = GrafikPenceresi(urun_adi, parent)
    grafik_penceresi.show()
    return grafik_penceresi

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Test için örnek ürün
    test_pencere = GrafikPenceresi("iPhone 14 ")
    test_pencere.show()
    
    sys.exit(app.exec_())