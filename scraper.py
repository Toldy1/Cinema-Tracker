import os
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
SCRAPER_API_KEY = "85461d0ec7d5dc5095eca191d8d2aece"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
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
            # ضفنا render=true و premium=true لكسر حماية الجافا سكريبت
            api_url = f"http://api.scraperapi.com/?api_key={SCRAPER_API_KEY}&url={url}&render=true&premium=true"
            
            # زدنا الوقت لـ 90 ثانية لأن المتصفح الوسيط ياخذ وقت باش يحل اللغز
            response = requests.get(api_url, timeout=90)
            
            if response.status_code == 200:
                html_content = response.text
                
                found_any = False
                for movie in target_movies:
                    if movie.lower() in html_content.lower():
                        send_telegram_message(f"🚨 تذاكر فيلم {movie} نزلت! \nالمصدر: {url}")
                        found_any = True
                        
                if not found_any:
                    print(f"تم فحص {url} بنجاح عبر ScraperAPI - لا توجد تذاكر حالياً.")
            else:
                send_telegram_message(f"⚠️ الموقع الوسيط رد بكود خطأ: {response.status_code} للرابط {url}")

        except Exception as e:
            send_telegram_message(f"❌ خطأ مع {url}: \n{str(e)}")

if __name__ == "__main__":
    check_tickets()
