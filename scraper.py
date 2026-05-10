import os
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CH_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to telegram: {e}")

def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    
    # ضفنا فيلم the backrooms للقائمة
    target_movies = ["dune", "spider-man", "spiderman", "doomsday", "odyssey", "backrooms", "the backrooms", "hokum"]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            html_content = response.text.lower()
            
            # سطر التأكيد (تقدر تشوفه في الـ Logs)
            print(f"✅ تم فحص الصفحة بنجاح. عينة: {html_content[:300]}")

            found_any = False
            for movie in target_movies:
                if movie in html_content:
                    send_telegram_message(f"🚨 عاجل: تذاكر فيلم {movie} نزلت في Marmara Forum! \nالرابط: {url}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص انتهى: الأفلام المطلوبة غير موجودة حالياً.")
        else:
            print(f"❌ فشل الاتصال: كود {response.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ: {e}")

if __name__ == "__main__":
    check_tickets()
