import sqlite3
from urunler import telefonlar,bilgisayarlar,tabletler,kulakliklar,kameralar,telefon_ozellikleri,bilgisayar_ozellikleri,tablet_ozellikleri,kulaklik_ozellikleri,kamera_ozellikleri
import hashlib

def veritabani_olustur():
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()
    
    imlec.execute("""
    CREATE TABLE IF NOT EXISTS kullanicilar (
        email TEXT PRIMARY KEY,
        sifre TEXT,
        cinsiyet TEXT,
        meslek TEXT,
        egitim TEXT,
        yas TEXT,
        boy TEXT,
        kilo TEXT
    )
    """)
    
    imlec.execute("""
    CREATE TABLE IF NOT EXISTS urunler (
        urun_turu TEXT, 
        marka TEXT,
        model TEXT,                      
        fiyat TEXT                     
    )
    """)

    baglanti.commit()
    baglanti.close()

def kullanici_ekle(email, sifre, cinsiyet, meslek, egitim, yas, boy, kilo):
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()
    hashli_sifre = sifreleri_hashle(sifre)
    
    imlec.execute("INSERT INTO kullanicilar VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                   (email, hashli_sifre, cinsiyet, meslek, egitim, yas, boy, kilo))
    
    baglanti.commit()
    baglanti.close()

def giris_kontrol(email, sifre):
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()
    hashli_sifre = sifreleri_hashle(sifre)
    
    imlec.execute("SELECT * FROM kullanicilar WHERE email=? AND sifre=?", (email, hashli_sifre))
    sonuc = imlec.fetchone()
    
    baglanti.close()
    return sonuc is not None

def kullanici_var_mi(email):
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()
    imlec.execute("SELECT * FROM kullanicilar WHERE email = ?",(email,))

    sonuc = imlec.fetchone()
    return sonuc is not None

def urun_ekle(urun_turu,marka,model,fiyat):
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()
    
    imlec.execute("INSERT INTO urunler VALUES (?, ?, ?, ?)", 
                   (urun_turu,marka,model,fiyat))
    
    baglanti.commit()
    baglanti.close()

def kullanici_profili_al(email):
    baglanti = sqlite3.connect("veritabani.db")
    imlec = baglanti.cursor()

    imlec.execute("SELECT * FROM kullanicilar WHERE email=?", (email))
    sonuc = imlec.fetchone()
    profil = {
        "cinsiyet": sonuc[0],
        "meslek": sonuc[1],
        "egitim": sonuc[2],
        "yas": sonuc[3],
        "boy": sonuc[4],
        "kilo": sonuc[5]
    }
    baglanti.close()
    return profil

def urunleri_veritabanindan_al():
        try:
            # Veritabanına bağlan
            baglanti = sqlite3.connect("veritabani.db")
            imlec = baglanti.cursor()

            # Verileri çek
            imlec.execute("SELECT * FROM urunler")
            urun_listesi = imlec.fetchall()  # Liste halinde döner

            return urun_listesi  # Liste olarak atandı

            baglanti.close()
        except Exception as e:
            print("Ürünleri veritabanından çekerken hata oluştu:", e)


def sifreleri_hashle(sifre):
    return hashlib.sha256(sifre.encode()).hexdigest()
