import sys
from PyQt5.QtCore import Qt, pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, \
    QMessageBox, QScrollArea, QMainWindow, QComboBox
from dotenv import load_dotenv
import os
import pandas as pd
import re
import google.generativeai as genai

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns # İsteğe bağlı, daha güzel grafikler için

import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- Ortam Değişkenleri ve API Anahtarları ---
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"C:\Users\WİN11\AppData\Local\Programs\Python\Python311\Lib\site-packages\PyQt5\Qt5\plugins\platforms"

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

DATA_DIR = 'data'
DATA_FILE_NAME = 'amazon_reviews_us_Wireless_v1_00.tsv'  # <<< KONTROL ET VE BU SATIRI DÜZENLE!
FILE_PATH = os.path.join(DATA_DIR, DATA_FILE_NAME)

df_products = None
stop_words = set(stopwords.words('english'))
analyzer = SentimentIntensityAnalyzer()

# --- Veri Yükleme ve Ön İşleme Fonksiyonları ---
class DataLoadThread(QThread):
    data_loaded = pyqtSignal(pd.DataFrame)
    load_error = pyqtSignal(str)

    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def preprocess_text(self, text):
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'<.*?>', '', text)
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        text = ' '.join(word for word in text.split() if word not in stop_words)
        return text

    def get_sentiment_score(self, text):
        if not isinstance(text, str) or not text.strip():
            return 0.0
        vs = analyzer.polarity_scores(text)
        return vs['compound']

    def run(self):
        try:
            print(f"\n--- Ürün verileri arka planda yükleniyor (ilk 10.000 satır) ---")
            df = pd.read_csv(
                self.file_path,
                delimiter='\t',
                on_bad_lines='skip',
                quoting=3,
                usecols=['product_id', 'product_title', 'product_category', 'star_rating', 'review_body'],
                nrows=10000  # Bu satırı önceki denemelerinizde 10000 olarak ayarlamıştık, öyle kalabilir.
            )

            df.columns = df.columns.str.lower().str.replace(' ', '_')
            df.rename(columns={
                'product_id': 'ProductID',
                'product_title': 'ProductName',
                'product_category': 'Category',
                'star_rating': 'Rating',
                'review_body': 'ReviewText'
            }, inplace=True)

            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
            df.dropna(subset=['Rating'], inplace=True)

            # CustomerID kaldırıldı
            df.dropna(subset=['ProductName', 'Category', 'ReviewText', 'ProductID'], inplace=True)
            df.fillna('', inplace=True)

            df['ProductName'] = df['ProductName'].astype(str).str.lower().str.strip()
            df['ReviewText'] = df['ReviewText'].astype(str).str.lower().str.strip()
            df['Category'] = df['Category'].astype(str).str.lower().str.strip()

            df['CleanedReviewText'] = df['ReviewText'].apply(self.preprocess_text)
            df['SentimentScore'] = df['ReviewText'].apply(self.get_sentiment_score)

            self.data_loaded.emit(df)
            print(f"Arka plan veri yüklemesi tamamlandı: {df.shape[0]} satır.")
        except FileNotFoundError:
            error_msg = f"Hata: Veri dosyası '{self.file_path}' bulunamadı. Lütfen dosya yolunu kontrol edin."
            print(error_msg)
            self.load_error.emit(error_msg)
        except Exception as e:
            error_msg = f"Ürün verileri yüklenirken bir hata oluştu: {e}"
            print(error_msg)
            self.load_error.emit(error_msg)

# --- Öneri Sistemi Fonksiyonları ---
def get_top_n_recommendations_chat(n=10, min_reviews=100):
    global df_products
    if df_products is None or df_products.empty:
        return pd.DataFrame()

    product_stats = df_products.groupby('ProductID').agg(
        average_rating=('Rating', 'mean'),
        review_count=('ReviewText', 'count'),
        product_name=('ProductName', 'first'),
        category=('Category', 'first')
    ).reset_index()

    popular_products = product_stats[product_stats['review_count'] >= min_reviews]
    top_n_products = popular_products.sort_values(by='average_rating', ascending=False)
    return top_n_products.head(n)

def create_rating_plot(category_name, data_frame, num_products=5):
    if data_frame is None or data_frame.empty:
        return None, "Veri bulunamadı."

    # Kullanıcının istediği kategoriye ait anahtar kelimeler
    category_keywords_map = {
        'telefon': ['phone', 'cellphone', 'smartphone', 'mobil', 'telefon'],
        'kulaklık': ['headphone', 'earbud', 'headset', 'kulaklık', 'earphones'],
        'kamera': ['camera', 'cam', 'kamera'],
        'tablet': ['tablet', 'ipad'],
        'speaker': ['speaker', 'hoparlör', 'ses'],
        'wireless': ['wireless', 'kablosuz', 'bluetooth']  # Genel Wireless kategorisi için
    }

    search_keywords = category_keywords_map.get(category_name.lower(), [category_name.lower()])

    condition = data_frame['Category'].str.contains(category_name, case=False, na=False)

    for keyword in search_keywords:
        condition = condition | \
                    data_frame['ProductName'].str.contains(r'\b' + re.escape(keyword) + r'\b', case=False, na=False,
                                                           regex=True) | \
                    data_frame['ReviewText'].str.contains(r'\b' + re.escape(keyword) + r'\b', case=False, na=False,
                                                          regex=True)

    filtered_data = data_frame[condition].copy()

    if filtered_data.empty:
        return None, f"'{category_name}' ile ilgili yeterli ürüne rastlanmadı. Kategori veya ürün adında eşleşme bulunamadı."

    product_stats = filtered_data.groupby('ProductID').agg(
        average_rating=('Rating', 'mean'),
        review_count=('ReviewText', 'count'),
        product_name=('ProductName', 'first'),
        category=('Category', 'first')
    ).reset_index()

    min_reviews_for_plot = 5
    popular_in_category = product_stats[product_stats['review_count'] >= min_reviews_for_plot]

    if popular_in_category.empty:
        return None, f"'{category_name}' ile ilgili yeterli yoruma sahip ürün bulunamadı. (Min. {min_reviews_for_plot} yorum)"

    top_products_for_plot = popular_in_category.sort_values(by='average_rating', ascending=False).head(num_products)

    if top_products_for_plot.empty:
        return None, f"'{category_name}' ile ilgili grafik oluşturulacak ürün bulunamadı."

    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(x='product_name', y='average_rating', data=top_products_for_plot, ax=ax, palette='viridis')

    ax.set_title(f"En Yüksek Puanlı {category_name.capitalize()} Ürünleri (İlk {num_products})", fontsize=16)
    ax.set_xlabel("Ürün Adı", fontsize=12)
    ax.set_ylabel("Ortalama Puan", fontsize=12)
    ax.set_ylim(0, 5.0)
    plt.xticks(rotation=60, ha='right', fontsize=10)
    plt.tight_layout()

    return fig, None

def get_filtered_recommendations_chat(query, num_results=5):
    global df_products
    if df_products is None or df_products.empty:
        return []

    query_lower = query.lower().strip()
    query_lower_safe = re.escape(query_lower)

    filtered_products = df_products[
        df_products['ProductName'].str.contains(query_lower_safe, na=False, regex=True) |
        df_products['ReviewText'].str.contains(query_lower_safe, na=False, regex=True) |
        df_products['Category'].str.contains(query_lower_safe, na=False, regex=True)
        ].copy()

    if filtered_products.empty:
        return []

    filtered_products_agg = filtered_products.groupby('ProductID').agg(
        product_name=('ProductName', 'first'),
        category=('Category', 'first'),
        average_rating=('Rating', 'mean'),
        review_count=('ReviewText', 'count')
    ).reset_index()

    filtered_products_agg = filtered_products_agg.sort_values(
        by=['average_rating', 'review_count'],
        ascending=[False, False]
    )
    return filtered_products_agg.head(num_results).to_dict('records')

# --- Chat Penceresi Sınıfı ---
class EntegreChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1600, 900)
        self.setWindowTitle("Alışveriş Asistanı")
        self.setWindowIcon(QIcon("robot.png"))

        self.konusma_gecmisi = []
        self.last_query_category = ""

        # Kullanıcı bilgileri (degiskenler modülünden)
        try:
            import degiskenler
            self.kullanici_email = degiskenler.giris_yapan_email
            from girisEkrani import kullanici_profili_al
            self.profil = kullanici_profili_al(self.kullanici_email)
        except:
            self.kullanici_email = "test@example.com"
            self.profil = {}

        try:
            if not GEMINI_API_KEY:
                raise ValueError("API_KEY .env dosyasında bulunamadı. Lütfen kontrol edin.")
            genai.configure(api_key=GEMINI_API_KEY)
            self.model = genai.GenerativeModel("models/gemini-2.0-flash")
            self.chat_session = self.model.start_chat(history=[])
        except Exception as e:
            QMessageBox.critical(self, "API Hatası",
                                 f"Gemini API yapılandırılamadı: {e}\nLütfen .env dosyasındaki API anahtarınızı kontrol edin.")
            self.model = None
            self.chat_session = None

        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.typeNextChar)
        self.typing_index = 0
        self.typing_text = ""

        self.initUI()
        self.start_data_loading()
        self.gecmisi_yukle()

    def initUI(self):
        # degiskenler import edildiğinden emin ol
        try:
            import degiskenler
        except:
            # Dummy degiskenler oluştur
            class DummyDegiskenler:
                baslik_fontu = QFont("Arial", 16, QFont.Bold)
                yazi_fontu = QFont("Arial", 10)
                buton_fontu = QFont("Arial", 12, QFont.Bold)
                urun_listesi = ["Telefon", "Laptop", "Tablet", "Kulaklık", "Kamera"]
                butce_listesi = ["-", "0-5000 TL", "5000-15000 TL", "15000-30000 TL", "30000+ TL"]
                tum_markalar = ["Farketmez", "Samsung", "Apple", "Xiaomi", "Huawei", "Nokia"]
                tum_kullanim_amaclari = ["Genel Kullanım", "İş", "Oyun", "Fotoğraf", "Müzik"]
                marka_listeleri = {
                    "Telefon": ["Farketmez", "Samsung", "Apple", "Xiaomi", "Huawei"],
                    "Laptop": ["Farketmez", "Dell", "HP", "Lenovo", "Asus"],
                    "Tablet": ["Farketmez", "Apple", "Samsung", "Huawei"],
                    "Kulaklık": ["Farketmez", "Sony", "Bose", "JBL", "Beats"],
                    "Kamera": ["Farketmez", "Canon", "Nikon", "Sony", "Fujifilm"]
                }
                kullanim_amaci_listeleri = {
                    "Telefon": ["Genel Kullanım", "İş", "Oyun", "Fotoğraf"],
                    "Laptop": ["Genel Kullanım", "İş", "Oyun", "Grafik"],
                    "Tablet": ["Genel Kullanım", "Okuma", "Çizim", "İş"],
                    "Kulaklık": ["Müzik", "Oyun", "İş", "Spor"],
                    "Kamera": ["Fotoğraf", "Video", "Profesyonel", "Hobi"]
                }
            degiskenler = DummyDegiskenler()

        font = QFont("Arial", 10)

        # Ana başlık
        self.yazi = QLabel("Alışverişle ilgili istediğinizi sorun: ", self)
        self.yazi.setFont(degiskenler.yazi_fontu)
        self.yazi.setGeometry(300, 20, 400, 30)

        # Metin kutusu
        self.yazi_kutusu = QTextEdit(self)
        self.yazi_kutusu.setFont(font)
        self.yazi_kutusu.setGeometry(300, 55, 1200, 300)
        self.yazi_kutusu.setPlaceholderText("Bugün ne aramak isterdiniz? (örn: 'telefon', 'bluetooth kulaklık') veya 'en popüler' yazın...")

        # Sol taraf filtre alanları
        # Ürün seçimi
        self.urun_yazisi = QLabel("Ürün: ", self)
        self.urun_yazisi.setFont(degiskenler.yazi_fontu)
        self.urun_yazisi.setGeometry(40, 60, 70, 40)

        self.urun_kutusu = QComboBox(self)
        self.urun_kutusu.addItems(degiskenler.urun_listesi)
        self.urun_kutusu.setFont(degiskenler.yazi_fontu)
        self.urun_kutusu.setGeometry(90, 55, 202, 50)
        self.urun_kutusu.currentTextChanged.connect(self.urun_degistir)

        # Bütçe seçimi
        self.butce_yazisi = QLabel("Bütçe: ", self)
        self.butce_yazisi.setFont(degiskenler.yazi_fontu)
        self.butce_yazisi.setGeometry(30, 135, 70, 40)

        self.butce_kutusu = QComboBox(self)
        self.butce_kutusu.addItems(degiskenler.butce_listesi)
        self.butce_kutusu.setFont(degiskenler.yazi_fontu)
        self.butce_kutusu.setGeometry(90, 130, 202, 50)

        # Marka seçimi
        self.marka_yazisi = QLabel("Marka: ", self)
        self.marka_yazisi.setFont(degiskenler.yazi_fontu)
        self.marka_yazisi.setGeometry(25, 210, 70, 40)

        self.marka_kutusu = QComboBox(self)
        self.marka_kutusu.addItems(degiskenler.tum_markalar)
        self.marka_kutusu.setFont(degiskenler.yazi_fontu)
        self.marka_kutusu.setGeometry(90, 210, 202, 50)

        # Kullanım amacı
        self.kullanim_yazisi = QLabel("Kullanım: ", self)
        self.kullanim_yazisi.setFont(degiskenler.yazi_fontu)
        self.kullanim_yazisi.setGeometry(10, 280, 80, 40)

        self.kullanim_kutusu = QComboBox(self)
        self.kullanim_kutusu.addItems(degiskenler.tum_kullanim_amaclari)
        self.kullanim_kutusu.setFont(degiskenler.yazi_fontu)
        self.kullanim_kutusu.setGeometry(90, 280, 202, 50)

        # Gönder butonu
        self.mesaj_butonu = QPushButton("Gönder", self)
        self.mesaj_butonu.setGeometry(300, 370, 150, 50)
        self.mesaj_butonu.setFont(degiskenler.buton_fontu)
        self.mesaj_butonu.clicked.connect(self.send_message)

        # Sonuç kutusu
        self.sonuc_kutusu = QTextEdit(self)
        self.sonuc_kutusu.setReadOnly(True)
        self.sonuc_kutusu.setFont(font)
        self.sonuc_kutusu.setGeometry(300, 440, 1200, 450)
        self.sonuc_kutusu.append("Asistan: Merhaba! Alışveriş asistanına hoş geldiniz.")
        self.sonuc_kutusu.append("Asistan: Ürün verileri yükleniyor, lütfen bekleyiniz...")

        # Alt kısım butonları
        self.cikis_butonu = QPushButton("Çıkış Yap", self)
        self.cikis_butonu.setGeometry(50, 800, 150, 50)
        self.cikis_butonu.setFont(degiskenler.buton_fontu)
        self.cikis_butonu.clicked.connect(self.cikis_yap)

        self.temizleme_butonu = QPushButton("Sohbeti Sil", self)
        self.temizleme_butonu.setGeometry(50, 725, 150, 50)
        self.temizleme_butonu.setFont(degiskenler.buton_fontu)
        self.temizleme_butonu.clicked.connect(self.sohbet_gecmisini_temizle)

        # Grafik Alanı
        self.graph_widget = QWidget(self)
        self.graph_widget.setGeometry(300, 680, 800, 200)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.graph_widget.setVisible(False)

        # Grafik Butonu
        self.show_graph_button = QPushButton("Puan Grafiğini Göster", self)
        self.show_graph_button.setGeometry(500, 370, 300, 50)
        self.show_graph_button.setFont(degiskenler.buton_fontu)
        self.show_graph_button.clicked.connect(self.request_graph_from_button)
        self.show_graph_button.setVisible(False)

    def urun_degistir(self, secilen_urun):
        try:
            import degiskenler
            self.marka_kutusu.clear()
            self.kullanim_kutusu.clear()
            
            self.marka_kutusu.addItems(degiskenler.marka_listeleri.get(secilen_urun, ["Farketmez"]))
            self.kullanim_kutusu.addItems(degiskenler.kullanim_amaci_listeleri.get(secilen_urun, ["Genel Kullanım"]))
        except:
            pass

    def show_graph(self, fig):
        # Önceki grafiği temizle
        for i in reversed(range(self.graph_layout.count())):
            widget_to_remove = self.graph_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)
                widget_to_remove.deleteLater()

        if fig:
            canvas = FigureCanvas(fig)
            self.graph_layout.addWidget(canvas)
            self.graph_widget.setVisible(True)
            plt.close(fig)
        else:
            self.graph_widget.setVisible(False)

    def request_graph_from_button(self):
        if self.last_query_category:
            self.konusma_gecmisi.append(
                f"<b><span style='color:#007bff;'>Siz:</span></b> '{self.last_query_category.capitalize()}' kategorisi için puan grafiğini göster.")
            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
            QApplication.processEvents()

            fig, error_msg = create_rating_plot(self.last_query_category, df_products)
            if fig:
                self.show_graph(fig)
                self.konusma_gecmisi.append(
                    f"<b><span style='color:#28a745;'>Asistan:</span></b> '{self.last_query_category.capitalize()}' kategorisindeki en yüksek puanlı ürünlerin grafiği yukarıda gösterilmiştir.")
            else:
                self.show_graph(None)
                self.konusma_gecmisi.append(
                    f"<b><span style='color:#dc3545;'>Asistan:</span></b> Grafik oluşturulamadı: {error_msg}")

            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
            self.sonuc_kutusu.verticalScrollBar().setValue(self.sonuc_kutusu.verticalScrollBar().maximum())
        else:
            QMessageBox.information(self, "Bilgi", "Önce bir kategori veya ürün hakkında arama yapmalısınız.")

    def start_data_loading(self):
        global df_products
        if df_products is None:
            self.data_thread = DataLoadThread(FILE_PATH)
            self.data_thread.data_loaded.connect(self.on_data_loaded)
            self.data_thread.load_error.connect(self.on_data_load_error)
            self.data_thread.start()
        else:
            self.sonuc_kutusu.append("Asistan: Ürün verileri zaten yüklü.")
            self.sonuc_kutusu.append(
                "Asistan: Nasıl yardımcı olabilirim? (Örn: 'en popüler', 'telefon', 'bluetooth kulaklık')")

    def on_data_loaded(self, df):
        global df_products
        df_products = df
        self.sonuc_kutusu.append("Asistan: Ürün verileri başarıyla yüklendi!")
        self.sonuc_kutusu.append(
            "Asistan: Nasıl yardımcı olabilirim? (Örn: 'en popüler', 'telefon', 'bluetooth kulaklık')")

    def on_data_load_error(self, error_msg):
        self.sonuc_kutusu.append(f"Asistan: Veri yüklenirken bir hata oluştu: {error_msg}")
        self.sonuc_kutusu.append(
            "Asistan: Maalesef şu anda ürün önerileri sunamıyorum. Lütfen uygulama geliştiricisiyle iletişime geçin.")

    def send_message(self):
        user_message = self.yazi_kutusu.toPlainText().strip()
        if not user_message:
            return

        self.konusma_gecmisi.append(f"<b><span style='color:#007bff;'>Siz:</span></b> {user_message}")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        self.yazi_kutusu.clear()

        self.konusma_gecmisi.append(f"<b><span style='color:#6c757d;'>Asistan:</span></b> Yanıtınız hazırlanıyor...")
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        QApplication.processEvents()

        # Chat kaydetme
        self.sohbeti_kaydet(user_message, "")

        # Gemini'ye gönder
        self.process_message_with_gemini(user_message)

    def process_message_with_gemini(self, message):
        if self.chat_session is None:
            self.konusma_gecmisi[
                -1] = f"<b><span style='color:#dc3545;'>Asistan:</span></b> API başlatılamadı. Lütfen API anahtarınızı kontrol edin."
            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
            return

        bot_response_text = ""
        message_lower = message.lower()

        if df_products is None or df_products.empty:
            bot_response_text = "Ürün verileri henüz yüklenmedi veya yüklenirken hata oluştu. Lütfen biraz bekleyin veya uygulamayı yeniden başlatın."
            self.konusma_gecmisi[-1] = f"<b><span style='color:#dc3545;'>Asistan:</span></b> {bot_response_text}"
            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
            return

        # Grafik butonunu başlangıçta gizle
        self.show_graph_button.setVisible(False)
        self.show_graph(None)

        if "en popüler" in message_lower:
            recommendations = get_top_n_recommendations_chat(n=10, min_reviews=100)
            if not recommendations.empty:
                bot_response_text = "İşte en popüler ürünlerden bazıları (min. 100 yorum ile):\n"
                for idx, row in recommendations.iterrows():
                    product_name_display = row['product_name'][:70] + "..." if len(row['product_name']) > 70 else row[
                        'product_name']
                    bot_response_text += f"- {product_name_display} (Puan: {row['average_rating']:.2f}, Yorum: {row['review_count']})\n"
            else:
                bot_response_text = "Üzgünüm, şu an için popüler ürün bulunamadı."
            self.last_query_category = ""

        elif "çıkış" in message_lower or "güle güle" in message_lower or "giriş ekranına dön" in message_lower:
            bot_response_text = "Güle güle! Tekrar bekleriz. Giriş ekranına dönülüyor..."
            QTimer.singleShot(1000, self.cikis_yap)
            self.last_query_category = ""

        else:
            # Gemini'ye gönderilecek prompt - chat.py'den alınan format
            all_categories = df_products['Category'].unique()
            top_categories = pd.Series(all_categories).value_counts().head(50).index.tolist()
            categories_str = ", ".join(top_categories)

            sample_popular_products = get_top_n_recommendations_chat(n=10, min_reviews=50)

            product_examples_str = ""
            if not sample_popular_products.empty:
                product_examples_str = "\nBazı popüler ürün örnekleri (Kategori - Ürün Adı):\n"
                for idx, row in sample_popular_products.iterrows():
                    product_examples_str += f"- {row['category']} - {row['product_name']}\n"

            # Chat.py'den alınan gelişmiş prompt yapısı
            prompt_text = f"""
            Sen bir alışveriş asistanısın. Kullanıcının talebini en iyi şekilde karşılamak için aşağıdaki talimatları takip et:
            1. Kullanıcının isteğini dikkatlice analiz et.
            2. **Veritabanı Bilgisi:** Şu anda {categories_str} gibi kategorilerde ürünlerimiz bulunmaktadır. Özellikle 'wireless' kategorisinde telefon, tablet aksesuarı, bluetooth cihazlar, kılıflar, kulaklıklar gibi birçok ürün bulunmaktadır.
            3. Eğer isteği genel bir ürün kategorisiyle ilgiliyse (örn. "telefon", "kulaklık"), genel bilgilerinden veya VERİLEN ÜRÜN LİSTESİNDEN yola çıkarak öneriler sun.
            4. Kullanıcıya önerdiğin ürünler hakkında kısa ve öz bilgi ver (örn. ne tür bir telefon, öne çıkan özellikleri).
            5. Eğer belirli bir ürün veya kategori bulamazsan, kullanıcıdan daha spesifik bilgi (bütçe, marka, özellik) isteyerek yardımcı ol.
            6. Cevaplarını doğrudan ve bilgilendirici ver, sohbet havasında tut.

            **Kullanıcı Özellikleri:**
            - Cinsiyet: {self.profil.get('cinsiyet', 'Belirtilmemiş')}
            - Yaş: {self.profil.get('yas', 'Belirtilmemiş')}
            - Meslek: {self.profil.get('meslek', 'Belirtilmemiş')}
            - Eğitim: {self.profil.get('egitim', 'Belirtilmemiş')}
            - Boy: {self.profil.get('boy', 'Belirtilmemiş')}
            - Kilo: {self.profil.get('kilo', 'Belirtilmemiş')}

            **Ürün Filtreleri:**
            - İstediği ürün: {self.urun_kutusu.currentText()}
            - Kullanım amacı: {self.kullanim_kutusu.currentText()}
            - Bütçe: {self.butce_kutusu.currentText()} (Eğer bütçe kısmı sadece '-' olarak gelirse bütçe öğrenmek için soru sorabilirsin)
            - Marka Tercihi: {self.marka_kutusu.currentText()} (Eğer marka kısmı 'Farketmez' olursa ekstra marka sorma)

            VERİLEN ÜRÜN LİSTESİNDEN BAZI ÖRNEKLER:
            {product_examples_str}

            Kullanıcının isteği: "{message}"

            Senin yanıtın:
            """

            try:
                gemini_response = self.chat_session.send_message(prompt_text)
                gemini_text = gemini_response.text

                # Anahtar kelime analizi ve veri setinden ürün çekme
                keywords_to_search = set()
                category_keywords = {
                    'telefon': ['phone', 'cellphone', 'smartphone', 'mobil'],
                    'kulaklık': ['headphone', 'earbud', 'headset', 'kulaklık', 'earphones'],
                    'kılıf': ['case', 'cover', 'shell', 'kılıf'],
                    'şarj': ['charger', 'charging', 'şarj', 'adapter'],
                    'tablet': ['tablet', 'ipad'],
                    'bilgisayar': ['computer', 'laptop', 'pc', 'notebook', 'dizüstü bilgisayar'],
                    'kamera': ['camera', 'cam', 'webcam', 'görüntü'],
                    'wireless': ['wireless', 'kablosuz', 'bluetooth', 'wifi'],
                    'ekran koruyucu': ['screen protector', 'guard', 'ekran koruyucu'],
                    'speaker': ['speaker', 'hoparlör', 'ses sistemi']
                }
                common_brands = ['samsung', 'apple', 'xiaomi', 'nokia', 'blu', 'realme', 'poco', 'vestel', 'huawei',
                                 'general mobile', 'lg', 'htc', 'sony', 'jbl', 'bose', 'anker']

                text_to_analyze = (message_lower + " " + gemini_text.lower()).lower()

                detected_category = ""
                for primary_key, variations in category_keywords.items():
                    if any(v in text_to_analyze for v in variations):
                        keywords_to_search.add(primary_key)
                        if not detected_category:
                            detected_category = primary_key

                for brand in common_brands:
                    if brand in text_to_analyze:
                        keywords_to_search.add(brand)

                self.last_query_category = detected_category if detected_category else ""

                # Telefon özel durumu
                if 'telefon' in keywords_to_search and 'wireless' in df_products['Category'].unique():
                    phone_related_wireless_products_df = df_products[
                        (df_products['Category'].str.contains('wireless', case=False, na=False)) &
                        (
                                df_products['ProductName'].str.contains(
                                    r'phone|cellphone|smartphone|kılıf|case|ekran koruyucu|charger|headphone|kulaklık',
                                    case=False, na=False, regex=True) |
                                df_products['ReviewText'].str.contains(
                                    r'phone|cellphone|smartphone|kılıf|case|ekran koruyucu|charger|headphone|kulaklık',
                                    case=False, na=False, regex=True)
                        )
                        ].drop_duplicates(subset=['ProductID'])

                    if not phone_related_wireless_products_df.empty:
                        keywords_to_search.add('phone_accessory_wireless')

                filtered_product_results_str = ""
                unique_products_found = set()

                for keyword in keywords_to_search:
                    if keyword == 'phone_accessory_wireless':
                        found_products_list = phone_related_wireless_products_df.head(5).to_dict('records')
                        for product in found_products_list:
                            product_id = product['ProductID']
                            if product_id not in unique_products_found:
                                unique_products_found.add(product_id)
                                product_name_display = product['ProductName'][:70] + "..." if len(
                                    product['ProductName']) > 70 else product['ProductName']
                                filtered_product_results_str += (f"- Ürün: {product_name_display}\n"
                                                                 f"  Kategori: {product['Category']}\n"
                                                                 f"  Puan: {product['Rating']:.2f} (Veri setinden)\n"
                                                                 f"--------------------\n")
                    else:
                        found_products_list = get_filtered_recommendations_chat(keyword, num_results=3)

                        for product in found_products_list:
                            product_id = product['ProductID']
                            if product_id not in unique_products_found:
                                unique_products_found.add(product_id)
                                product_name_display = product['product_name'][:70] + "..." if len(
                                    product['product_name']) > 70 else product['product_name']
                                rating_val = product.get('average_rating', product.get('Rating', 0.0))
                                review_count_val = product.get('review_count', 0)

                                filtered_product_results_str += (f"- Ürün: {product_name_display}\n"
                                                                 f"  Kategori: {product['category']}\n"
                                                                 f"  Puan: {rating_val:.2f} ({review_count_val} yorum)\n"
                                                                 f"--------------------\n")

                if filtered_product_results_str:
                    if "maalesef şu anda" in gemini_text.lower() or "üzgünüm, isteğinizle eşleşen bir ürün bulamadım." in gemini_text.lower():
                        bot_response_text = "Veri tabanımızda bulduğum, isteğinizle ilgili bazı ürünler:\n" + filtered_product_results_str
                        if "ek bilgiye ihtiyacım var" not in gemini_text.lower():
                            bot_response_text += "\n" + gemini_text
                    else:
                        bot_response_text = gemini_text + "\n\n**Ayrıca veri tabanımızda bulduğum ilgili ürünler:**\n" + filtered_product_results_str

                    if self.last_query_category:
                        self.show_graph_button.setVisible(True)
                else:
                    bot_response_text = gemini_text

                # Chat kayıt güncelleme
                self.sohbeti_kaydet(message, bot_response_text, update_last=True)

            except Exception as e:
                print(f"Gemini API çağrısı hatası: {e}")
                bot_response_text = f"Üzgünüm, şu an yanıt veremiyorum. Bir sorun oluştu (API Hatası: {type(e).__name__}). Lütfen internet bağlantınızı ve API anahtarınızı kontrol edin."

        # Typing efekti başlat
        self.konusma_gecmisi[-1] = f"<b><span style='color:#28a745;'>Asistan:</span></b> "
        self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))

        self.typing_text = bot_response_text
        self.typing_index = 0
        self.typing_timer.start(15)

    def sohbeti_kaydet(self, kullanici_girdi, asistan_cevabi, update_last=False):
        try:
            dosya_adi = f"gecmisler/{self.kullanici_email}.txt"
            os.makedirs("gecmisler", exist_ok=True)
            
            if update_last and asistan_cevabi:
                # Dosyayı oku ve son asistan cevabını güncelle
                if os.path.exists(dosya_adi):
                    with open(dosya_adi, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                    
                    # Son "Asistan:" satırını bul ve güncelle
                    for i in range(len(lines) - 1, -1, -1):
                        if lines[i].startswith("Asistan:"):
                            lines[i] = f"Asistan: {asistan_cevabi}\n"
                            break
                    
                    with open(dosya_adi, "w", encoding="utf-8") as f:
                        f.writelines(lines)
            else:
                with open(dosya_adi, "a", encoding="utf-8") as f:
                    f.write(f"Kullanıcı: {kullanici_girdi}\n")
                    if asistan_cevabi:
                        f.write(f"Asistan: {asistan_cevabi}\n\n")
        except Exception as e:
            print(f"Sohbet kaydetme hatası: {e}")

    def gecmisi_yukle(self):
        try:
            dosya_adi = f"gecmisler/{self.kullanici_email}.txt"
            if os.path.exists(dosya_adi):
                with open(dosya_adi, "r", encoding="utf-8") as f:
                    gecmis = f.read()
                    if gecmis.strip():
                        gecmis_lines = gecmis.splitlines()
                        formatted_history = []
                        for line in gecmis_lines:
                            if line.startswith("Kullanıcı:"):
                                formatted_history.append(f"<b><span style='color:#007bff;'>Siz:</span></b> {line[10:]}")
                            elif line.startswith("Asistan:"):
                                formatted_history.append(f"<b><span style='color:#28a745;'>Asistan:</span></b> {line[9:]}")
                            elif line.strip():
                                formatted_history.append(line)
                        
                        if formatted_history:
                            self.konusma_gecmisi.extend(formatted_history)
                            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
        except Exception as e:
            print(f"Geçmiş yükleme hatası: {e}")

    def sohbet_gecmisini_temizle(self):
        try:
            self.konusma_gecmisi.clear()
            self.sonuc_kutusu.clear()
            
            # Dosyayı da temizle
            dosya_adi = f"gecmisler/{self.kullanici_email}.txt"
            if os.path.exists(dosya_adi):
                os.remove(dosya_adi)
                
            self.sonuc_kutusu.append("Asistan: Sohbet geçmişi temizlendi.")
            self.sonuc_kutusu.append("Asistan: Nasıl yardımcı olabilirim?")
        except Exception as e:
            print(f"Sohbet temizleme hatası: {e}")

    def typeNextChar(self):
        if self.typing_index < len(self.typing_text):
            metin = self.typing_text[:self.typing_index + 1]
            full_html = "<br><br>".join(self.konusma_gecmisi[:-1]) + f"<br><br><b><span style='color:#28a745;'>Asistan:</span></b> {metin}"
            self.sonuc_kutusu.setHtml(full_html)
            self.sonuc_kutusu.verticalScrollBar().setValue(self.sonuc_kutusu.verticalScrollBar().maximum())
            self.typing_index += 1
        else:
            self.konusma_gecmisi[-1] += self.typing_text
            self.sonuc_kutusu.setHtml("<br><br>".join(self.konusma_gecmisi))
            self.sonuc_kutusu.verticalScrollBar().setValue(self.sonuc_kutusu.verticalScrollBar().maximum())
            self.typing_timer.stop()

    def cikis_yap(self):
        from girisEkrani import LoginRegisterWindow
        cevap = QMessageBox.question(self, "Çıkış Yap", "Giriş ekranına dönmek istiyor musunuz?",
                                     QMessageBox.Yes | QMessageBox.No)
        if cevap == QMessageBox.Yes:
            try:
                self.login_window = LoginRegisterWindow()
                self.login_window.show()
                self.close()
            except Exception as e:
                print(f"Giriş ekranına dönüş hatası: {e}")
                self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = EntegreChatWindow()
    chat_window.show()
    sys.exit(app.exec_())