import google.generativeai as genai

genai.configure(api_key="AIzaSyD0LaOPGVQ8QpvywZ3KlQRV6fyqrSJqc_w")

model = genai.GenerativeModel("models/gemini-2.0-flash")

# Chat oturumu başlat (parametresiz)
chat = model.start_chat()

# Sistem mesajı ile başlangıç bağlamı kurmak için ilk kullanıcı mesajı yerine bunu deneyebilirsin:
response = chat.send_message("Sen bir alışveriş asistanısın. Kullanıcının ihtiyaçlarını analiz edip ürün önerileri yapıyorsun.")

# Ardından gerçek kullanıcı mesajını gönder:
response = chat.send_message("500 TL altı spor ayakkabı önerir misin?")

print(response.text)
