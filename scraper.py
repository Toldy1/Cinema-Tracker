from playwright.sync_api import sync_playwright
import os
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

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

    # فتح متصفح كروم حقيقي في الخلفية
    with sync_playwright() as p:
        # headless=True معناها يشتغل في الخلفية بدون واجهة
        browser = p.chromium.launch(headless=True)
        # نحطوا معلومات متصفح طبيعي عشان نتخطوا الحماية
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        for url in urls:
            try:
                # يفتح الرابط ويستنى الصفحة تحمل بالكامل
                page.goto(url, timeout=60000)
                page.wait_for_load_state("networkidle", timeout=15000)
                
                # ياخذ الكود بتاع الصفحة بعد ما تفتح
                html_content = page.content()
                
                found_any = False
                for movie in target_movies:
                    if movie.lower() in html_content.lower():
                        send_telegram_message(f"🚨 تذاكر فيلم {movie} نزلت! \nالمصدر: {url}")
                        found_any = True
                        
                if not found_any:
                    print(f"تم فحص {url} بنجاح كمتصفح حقيقي - لا توجد تذاكر حالياً.")
                    
            except Exception as e:
                send_telegram_message(f"❌ خطأ مع {url}: \n{str(e)}")
        
        browser.close()

if __name__ == "__main__":
    check_tickets()
