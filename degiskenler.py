from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton

giris_durumu = False
giris_yapan_email = ""

# Modern font definitions
baslik_fontu = QFont("Segoe UI", 28, QFont.Bold)
yazi_fontu = QFont("Segoe UI", 14)
buton_fontu = QFont("Segoe UI", 16, QFont.Bold)

# ComboBox listeleri
meslek_listesi = ["Öğrenci", "Öğretmen", "Mühendis", "Doktor", "Avukat", "Hemşire", "Yazılımcı",
                "Tasarımcı", "Muhasebeci", "Serbest Meslek", "Ev Hanımı", "İşsiz", "Emekli", "Diğer"]

egitim_listesi = ["İlkokul", "Ortaokul", "Lise", "Ön Lisans", "Lisans", "Yüksek Lisans", "Doktora"]

yas_listesi = ["18 yaş altı","18-24","25-34","35-44","45-54","55-64","65 yaş ve üzeri"]

boy_listesi = ["150 cm altı","150-159 cm","160-169 cm","170-179 cm","180-189 cm","190 cm ve üzeri"]

kilo_listesi = ["45 kg altı","45-54 kg","55-64 kg","65-74 kg","75-84 kg","85-94 kg","95 kg ve üzeri"]

butce_listesi = ["-","1.000 TL altı","1.000 - 5.000 TL","5.000 - 7.500 TL","7.500 - 10.000 TL",
                "10.000 - 15.000 TL","15.000 - 20.000 TL","20.000 - 30.000 TL","30.000 - 50.000 TL","50.000 TL üzeri"]

urun_listesi = ["-","Bilgisayar","Kamera","Kulaklık","Tablet","Telefon"]

tum_markalar = ["Farketmez","Samsung","Apple","Xiaomi","Realme","Huawei","General Mobile","HP","MSI","Lenovo","Asus","Acer","MacBook","Monster","Reeder","Canon","Nikon","Sony","Fujifilm","Panasonic","JBL","Anker","Sennheiser"]

marka_listeleri = {
    "-": tum_markalar,
    "Telefon": ["Farketmez","Samsung", "Apple", "Xiaomi", "Realme", "Huawei", "General Mobile"],
    "Bilgisayar": ["Farketmez","HP","MSI", "Lenovo", "Asus", "Acer", "MacBook", "Monster"],
    "Tablet": ["Farketmez","Apple", "Samsung", "Huawei","Xiomi", "Reeder", "Lenovo","TCL","Casper"],
    "Kamera": ["Farketmez","Canon", "Nikon", "Sony", "Fujifilm", "Panasonic", "Olympus"],
    "Kulaklık": ["Farketmez","Sony", "JBL", "Apple", "Samsung", "Anker", "Sennheiser","Bose","Marshall","Xiomi","Huawei"],
}

tum_kullanim_amaclari = ["Farketmez","Günlük kullanım","Sosyal medya","Oyun","Fotoğrafçılık","Video izleme","İş için kullanım","Video düzenleme","Programlama","İş/çalışma","Grafik tasarım","Eğitim","Çocuk kullanımı","Kitap okuma","Hobi amaçlı","Profesyonel fotoğrafçılık","Vlog çekimi","Doğa çekimleri","Video prodüksiyon","Müzik dinleme","Spor","Film/dizi izleme","Ofis kullanımı"]

kullanim_amaci_listeleri = {
    "-": tum_kullanim_amaclari,
    "Telefon": [
        "Farketmez", "Günlük kullanım", "Sosyal medya", "Oyun", 
        "Fotoğrafçılık", "Video izleme", "İş/çalışma", 
    ],
    "Bilgisayar": [
        "Farketmez", "Oyun", "Video düzenleme", "Programlama", 
        "İş/çalışma", "Grafik tasarım", "Günlük kullanım", "Eğitim"
    ],
    "Tablet": [
        "Farketmez", "Video izleme", "Çocuk kullanımı", "Eğitim", 
        "Kitap okuma", "Sosyal medya", "Günlük kullanım"
    ],
    "Kamera": [
        "Farketmez", "Hobi amaçlı", "Profesyonel fotoğrafçılık", 
        "Vlog çekimi", "Doğa çekimleri", "Video prodüksiyon"
    ],
    "Kulaklık": [
        "Farketmez", "Müzik dinleme", "Oyun", "Spor", 
        "Film/dizi izleme", "Ofis kullanımı"
    ],
}

# MODERN BUTTON STİLLERİ
modern_buton_stili = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #667eea, stop:1 #764ba2);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #5a67d8, stop:1 #6b46c1);
        box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
        transform: translateY(-2px);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #4c51bf, stop:1 #553c9a);
        transform: translateY(0px);
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
    }
    QPushButton:disabled {
        background: #718096;
        color: #a0aec0;
        box-shadow: none;
    }
"""

modern_buton_stili_2 = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #f093fb, stop:1 #f5576c);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        box-shadow: 0 8px 32px rgba(240, 147, 251, 0.3);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #ed64a6, stop:1 #e53e3e);
        box-shadow: 0 12px 40px rgba(240, 147, 251, 0.5);
        transform: translateY(-2px);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #d53f8c, stop:1 #c53030);
        transform: translateY(0px);
        box-shadow: 0 4px 16px rgba(240, 147, 251, 0.3);
    }
"""

mode_button_style = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #4facfe, stop:1 #00f2fe);
        color: white;
        border: none;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        padding: 8px;
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #4299e1, stop:1 #00d4ff);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.6);
        transform: translateY(-2px);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                  stop:0 #3182ce, stop:1 #00b8d4);
        transform: translateY(0px);
    }
"""

# MODERN GLASSMORPHISM LINE EDIT STİLİ
modern_lineedit_stili = """
    QLineEdit {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 15px 20px;
        font-size: 14px;
        font-weight: 500;
        backdrop-filter: blur(10px);
        selection-background-color: rgba(102, 126, 234, 0.5);
        selection-color: white;
    }
    
    QLineEdit:focus {
        border: 2px solid rgba(102, 126, 234, 0.8);
        background: rgba(255, 255, 255, 0.25);
        outline: none;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    QLineEdit:hover {
        border: 2px solid rgba(255, 255, 255, 0.4);
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }
    
    QLineEdit:disabled {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    QLineEdit::placeholder {
        color: rgba(255, 255, 255, 0.6);
        font-style: italic;
    }
"""

# MODERN GLASSMORPHISM COMBOBOX STİLİ
modern_combobox_stili = """
    QComboBox {
        background: rgba(255, 255, 255, 0.15);
        color: white;
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        padding: 8px 15px;
        font-size: 16px;
        font-weight: 500;
        backdrop-filter: blur(10px);
        min-height: 25px;
    }
    
    QComboBox:hover {
        background: rgba(255, 255, 255, 0.25);
        border: 2px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.1);
    }
    
    QComboBox:focus {
        border: 2px solid rgba(102, 126, 234, 0.8);
        background: rgba(255, 255, 255, 0.3);
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
    }
    
    QComboBox:disabled {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border: none;
        background: transparent;
        border-top-right-radius: 15px;
        border-bottom-right-radius: 15px;
    }
    
    QComboBox::down-arrow {
        image: none;
        width: 0px;
        height: 0px;
        border-style: solid;
        border-width: 8px 6px 0px 6px;
        border-color: rgba(255, 255, 255, 0.8) transparent transparent transparent;
        margin-right: 8px;
    }
    
    QComboBox::down-arrow:hover {
        border-color: rgba(102, 126, 234, 0.8) transparent transparent transparent;
    }
    
    QComboBox QAbstractItemView {
        background: rgba(30, 30, 30, 0.95);
        color: white;
        border: 2px solid rgba(102, 126, 234, 0.5);
        border-radius: 10px;
        selection-background-color: rgba(102, 126, 234, 0.6);
        selection-color: white;
        padding: 5px;
        backdrop-filter: blur(20px);
        outline: none;
    }
    
    QComboBox QAbstractItemView::item {
        background: transparent;
        color: white;
        padding: 8px 15px;
        border-radius: 5px;
        margin: 2px;
    }
    
    QComboBox QAbstractItemView::item:hover {
        background: rgba(102, 126, 234, 0.4);
        color: white;
    }
    
    QComboBox QAbstractItemView::item:selected {
        background: rgba(102, 126, 234, 0.6);
        color: white;
    }
"""