import os
import requests as standard_requests
from curl_cffi import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        standard_requests.post(url, json=payload)
    except Exception as e:
        print(f"Error sending to telegram: {e}")

def check_tickets():
    urls = [
        "https://www.biletiva.com/tags/events?cat=sinema",
        "https://worldcinezone.com.tr/marmaraforum"
    ]
    target_movies = ["Dune", "Spider-Man", "Doomsday", "Odyssey"]

    for url in urls:
        try:
            # استخدام بصمة متصفح كروم 110 لتخطي جدار الحماية
            response = requests.get(url, impersonate="chrome110", timeout=30)
            
            if response.status_code == 200:
                html_content = response.text
                
                # التأكد إن الموقع ما حولناش لصفحة التأكيد الأمنية
                if "just a moment" in html_content.lower() or "cloudflare" in html_content.lower():
                    send_telegram_message(f"⚠️ تنبيه: الموقع {url} طلب تحقق بشري (CAPTCHA) ومسّكر على سيرفرات الكلاود.")
                    continue

                found_any = False
                for movie in target_movies:
                    if movie.lower() in html_content.lower():
                        send_telegram_message(f"🚨 تذاكر فيلم {movie} نزلت! \nالمصدر: {url}")
                        found_any = True
                        
                if not found_any:
                    print(f"تم فحص {url} بنجاح - لا توجد تذاكر حالياً.")
            else:
                send_telegram_message(f"⚠️ كود خطأ {response.status_code} من الرابط {url}")
                
        except Exception as e:
            send_telegram_message(f"❌ خطأ مع {url}: \n{str(e)}")

if __name__ == "__main__":
    check_tickets()
