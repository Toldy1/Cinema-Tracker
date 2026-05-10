import cloudscraper
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
    # الروابط اللي نبي نتبعها
    urls = [
        "https://www.biletiva.com/tags/events?cat=sinema",
        "https://worldcinezone.com.tr/marmaraforum"
    ]
    
    # الأفلام المستهدفة
    target_movies = ["Dune", "Spider-Man", "Doomsday", "Odyssey"]
    
    scraper = cloudscraper.create_scraper()
    
    for url in urls:
        try:
            response = scraper.get(url, timeout=20)
            
            if response.status_code == 200:
                found_any = False
                for movie in target_movies:
                    if movie.lower() in response.text.lower():
                        send_telegram_message(f"🚨 تذاكر فيلم {movie} نزلت! \nالمصدر: {url}")
                        found_any = True
                
                # لو السكربت شغال وما لقى شي، مش حيدير شي (زي ما طلبت)
                if not found_any:
                    print(f"تم فحص {url} - لا توجد تذاكر حالياً.")
            
            else:
                # لو الموقع عطى خطأ (مثلاً حظر الـ IP)، يبعتلك تنبيه
                send_telegram_message(f"⚠️ مشكلة في التتبع! الموقع {url} رد بكود خطأ: {response.status_code}")

        except Exception as e:
            # لو الكود علق أو صار خطأ تقني، يبعتلك السبب
            send_telegram_message(f"❌ خطأ فني في سكربت التتبع للرابط {url}: \n{str(e)}")

if __name__ == "__main__":
    check_tickets()
