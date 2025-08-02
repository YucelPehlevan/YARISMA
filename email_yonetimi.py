import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def dogrulama_kodu_gonder(kime, gmail_adresi, gmail_sifresi):
    kod = str(random.randint(100000, 999999))  # 6 haneli kod

    mesaj = MIMEMultipart()
    mesaj['From'] = gmail_adresi
    mesaj['To'] = kime
    mesaj['Subject'] = "Alışveriş Asistanı - Doğrulama Kodu"

    body = f"Merhaba,\n\nKayıt işleminizi tamamlamak için doğrulama kodunuz: {kod}\n\nTeşekkürler."
    mesaj.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(gmail_adresi, gmail_sifresi)
        server.sendmail(gmail_adresi, kime, mesaj.as_string())
        server.quit()
        return kod
    except Exception as e:
        print("Mail gönderilemedi:", e)
        return None
