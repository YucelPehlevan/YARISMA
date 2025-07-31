import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# NLTK kaynaklarını indir (sadece bir kez çalıştırın)
# Eğer indirme yapmadıysanız, bu satırların burada kalması ve kodu bir kez çalıştırmanız yeterlidir.
try:
    nltk.data.find('corpora/stopwords')
except:
    nltk.download('stopwords')

try:
    nltk.data.find('sentiment/vader_lexicon')
except:
    nltk.download('vader_lexicon')

# Veri setlerinin bulunduğu klasör
DATA_DIR = 'data'

# BURAYI DİKKATLİCE KONTROL ET VE DÜZENLE:
# `data` klasörüne attığınız .tsv dosyaları arasında en büyük ve ana olanının adını buraya yazın.
# Muhtemelen 'amazon_reviews.tsv' veya 'US_reviews.tsv' gibi bir şeydir.
# Eğer birden fazla büyük .tsv varsa, ilk olarak en kapsamlı olduğunu düşündüğünüzü deneyin.
DATA_FILE_NAME = 'amazon_reviews_us_Wireless_v1_00.tsv' # <<< LÜTFEN BU SATIRI KENDİ DOSYA ADINIZLA DEĞİŞTİRİN!

FILE_PATH = os.path.join(DATA_DIR, DATA_FILE_NAME)

# İngilizce durma kelimelerini yükle
stop_words = set(stopwords.words('english'))
# VADER duygu analizörü
analyzer = SentimentIntensityAnalyzer()

def preprocess_text(text):
    """Metin verilerini temizler ve ön işler."""
    if not isinstance(text, str):
        return "" # Metin olmayan veya NaN değerler için boş string döndür
    text = text = text.lower() # Küçük harfe çevir
    text = re.sub(r'<.*?>', '', text) # HTML etiketlerini kaldır (bazı yorumlarda olabilir)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text) # Sadece harf, sayı ve boşluk bırak
    text = re.sub(r'\s+', ' ', text).strip() # Birden fazla boşluğu tek boşluğa indir ve boşlukları temizle
    text = ' '.join(word for word in text.split() if word not in stop_words) # Durma kelimelerini kaldır
    return text

def get_sentiment_score(text):
    """Metin için duygu analizi skoru hesaplar."""
    if not isinstance(text, str) or not text.strip():
        return 0.0 # Boş veya metin olmayan değerler için nötr kabul et
    vs = analyzer.polarity_scores(text)
    return vs['compound'] # Bileşik skor (-1.0 ile 1.0 arası, 1.0 en pozitif)

def load_and_preprocess_product_data(file_path):
    """Veri setini yükler, temizler ve ön işler."""
    if not os.path.exists(file_path):
        print(f"Hata: '{file_path}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        return None

    try:
        print(f"\n--- '{DATA_FILE_NAME}' yükleniyor ve ön işleniyor (ilk 100.000 satır) ---")
        # TSV dosyasını oku, delimiter olarak sekme kullanıyoruz
        # on_bad_lines='skip' hatalı satırları atlar. quoting=3 tırnak sorunlarını çözebilir.
        # nrows=100000 ile sadece ilk 100.000 satırı yüklüyoruz.
        df = pd.read_csv(file_path, delimiter='\t', on_bad_lines='skip', quoting=3, nrows=100000)

        # Sütun isimlerini küçük harfe çevirelim ve boşlukları alt çizgi yapalım
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # İhtiyacımız olan temel sütunlar:
        # product_id, product_title, product_category, star_rating, review_body
        # Bu sütun isimleri Kaggle sayfasındaki veri setinin yapısına göre belirlenmiştir.

        column_mapping = {
            'product_title': 'ProductName',
            'product_category': 'Category',
            'star_rating': 'Rating',
            'review_body': 'ReviewText',
            'product_id': 'ProductID',
            'customer_id': 'CustomerID'
        }

        # Önce sadece gerekli sütunları seçelim (veri setinde gerçekten var olanları)
        selected_columns = [col for col in column_mapping.keys() if col in df.columns]
        df = df[selected_columns]

        # Seçilen sütunları yeniden adlandır
        df.rename(columns=column_mapping, inplace=True)

        # Eksik değerleri yönetme: Temel bilgileri eksik olan satırları at
        # ProductName, Category, Rating, ReviewText, ProductID, CustomerID kritik öneme sahiptir.
        df.dropna(subset=['ProductName', 'Category', 'Rating', 'ReviewText', 'ProductID', 'CustomerID'], inplace=True)
        # Diğer eksik değerleri (örneğin 'Price' veya 'Brand' gibi eğer olsaydı) boş string ile doldur
        df.fillna('', inplace=True)

        # Puan sütununu sayısal formata dönüştür
        if 'Rating' in df.columns:
            df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
            df.dropna(subset=['Rating'], inplace=True) # Sayıya çevrilemezse o satırı at

        # Metin verilerini temizleme
        print("Yorum metinleri temizleniyor...")
        df['CleanedReviewText'] = df['ReviewText'].apply(preprocess_text)

        # Duygu skoru ekle
        print("Duygu skorları hesaplanıyor...")
        df['SentimentScore'] = df['ReviewText'].apply(get_sentiment_score)


        print("\nVeri ön işleme tamamlandı. İlk 5 satır:")
        print(df.head())
        print("\nİşlenmiş veri seti bilgisi:")
        print(df.info())
        print("\nEksik değerler (işlem sonrası):")
        print(df.isnull().sum())
        print("\nSütun isimleri (işlem sonrası):")
        print(df.columns.tolist())

        return df
    except Exception as e:
        print(f"Dosya yüklenirken ve işlenirken bir hata oluştu: {e}")
        return None

if __name__ == "__main__":
    processed_product_df = load_and_preprocess_product_data(FILE_PATH)
    if processed_product_df is not None:
        print("\nİşlenmiş ürün yorumları veri setiniz hazır.")

        # Örnek çıktılar
        print("\nEn yüksek puanlı 5 ürün yorumu:")
        # Sütun yoksa hata vermemek için kontrol ekleyelim
        if 'ProductName' in processed_product_df.columns and 'Rating' in processed_product_df.columns and 'ReviewText' in processed_product_df.columns:
            print(processed_product_df.sort_values(by='Rating', ascending=False)[['ProductName', 'Rating', 'ReviewText']].head().to_string())
        else:
            print("Gerekli sütunlar ('ProductName', 'Rating', 'ReviewText') bulunamadı.")


        print("\nEn pozitif duygu skoruna sahip 5 yorum:")
        if 'ProductName' in processed_product_df.columns and 'SentimentScore' in processed_product_df.columns and 'ReviewText' in processed_product_df.columns:
            print(processed_product_df.sort_values(by='SentimentScore', ascending=False)[['ProductName', 'SentimentScore', 'ReviewText']].head().to_string())
        else:
            print("Gerekli sütunlar ('ProductName', 'SentimentScore', 'ReviewText') bulunamadı.")

        print("\nPuan dağılımı (Rating sütunu):")
        if 'Rating' in processed_product_df.columns:
            print(processed_product_df['Rating'].value_counts().sort_index().to_string())
        else:
            print("'Rating' sütunu bulunamadı.")

        print("\nEn çok yorum alan ürünler (top 10 ProductID, yorum sayısı ve ortalama puan):")
        if 'ProductID' in processed_product_df.columns and 'ReviewText' in processed_product_df.columns and 'Rating' in processed_product_df.columns:
            product_summary = processed_product_df.groupby('ProductID').agg(
                num_reviews=('ReviewText', 'count'),
                avg_rating=('Rating', 'mean'),
                avg_sentiment=('SentimentScore', 'mean'),
                first_product_name=('ProductName', 'first')
            ).reset_index()
            product_summary = product_summary.sort_values(by='num_reviews', ascending=False)
            print(product_summary.head(10).to_string())
        else:
            print("Gerekli sütunlar (ProductID, ReviewText, Rating) bulunamadı.")

        print("\nKategori dağılımı (top 10):")
        if 'Category' in processed_product_df.columns:
            print(processed_product_df['Category'].value_counts().head(10).to_string())
        else:
            print("'Category' sütunu bulunamadı.")

        print(f"\nİşlenmiş veri seti boyutu: {processed_product_df.shape[0]} satır, {processed_product_df.shape[1]} sütun.")