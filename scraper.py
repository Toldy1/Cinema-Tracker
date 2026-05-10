import os
import requests

# جلب بيانات تليجرام من الأسرار
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"خطأ في إرسال رسالة تليجرام: {e}")

def check_tickets():
    # الروابط المستهدفة
    urls = [
        "https://www.biletiva.com/tags/events?cat=sinema",
        "https://worldcinezone.com.tr/marmaraforum"
    ]
    
    # الأفلام اللي نراجوا فيها
    target_movies = ["Dune", "Spider-Man", "Doomsday", "Odyssey"]
    
    for url in urls:
        try:
            # استخدام خدمة allorigins كوسيط لتخطي حظر السيرفرات
            proxy_url = f"https://api.allorigins.win/get?disableCache=true&url={url}"
            
            # حطينا وقت أطول شوية (30 ثانية) لأن الوسيط ياخذ وقت
            response = requests.get(proxy_url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                html_content = data.get("contents", "")
                
                if html_content:
                    found_any = False
                    for movie in target_movies:
                        if movie.lower() in html_content.lower():
                            send_telegram_message(f"🚨 تذاكر فيلم {movie} نزلت! \nالمصدر: {url}")
                            found_any = True
                    
                    if not found_any:
                        print(f"تم فحص {url} بنجاح - لا توجد تذاكر حالياً.")
                else:
                    print(f"لم يتم جلب محتوى من {url}")
            else:
                send_telegram_message(f"⚠️ الموقع الوسيط رد بكود خطأ: {response.status_code} للرابط {url}")

        except Exception as e:
            send_telegram_message(f"❌ خطأ فني في سكربت التتبع للرابط {url}: \n{str(e)}")

if __name__ == "__main__":
    check_tickets()
