import json
import os

DOSYA_YOLU = "veriler.json"

def dosyayi_oku():
    if not os.path.exists(DOSYA_YOLU):
        return {"kullanicilar": {}}
    with open(DOSYA_YOLU, "r", encoding="utf-8") as f:
        return json.load(f)

def dosyaya_yaz(veri):
    with open(DOSYA_YOLU, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

def kullanici_var_mi(email):
    veri = dosyayi_oku()
    return email in veri["kullanicilar"]

def kullanici_ekle(email, sifre, profil):
    veri = dosyayi_oku()
    veri["kullanicilar"][email] = {
        "sifre": sifre,
        **profil  # diğer bilgiler
    }
    dosyaya_yaz(veri)

def giris_kontrol(email, sifre):
    veri = dosyayi_oku()
    if email in veri["kullanicilar"]:
        return veri["kullanicilar"][email]["sifre"] == sifre
    return False

def kullanici_profili_al(email):
    veri = dosyayi_oku()
    return veri["kullanicilar"].get(email, {})