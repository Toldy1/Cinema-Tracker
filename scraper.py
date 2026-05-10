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
        "https://www.biletiva.com/sitemap.xml",
        "https://www.biletiva.com/tags/events?cat=sinema",
        "https://worldcinezone.com.tr/marmaraforum"
    ]
    
    target_movies = ["dune", "spider-man", "spiderman", "doomsday", "odyssey"]

    # استخدام بروكسي مجاني لتخطي حظر الـ IP
    # المواقع هذي بتجيب المحتوى كأنك داخل من مكان ثاني تماماً
    proxy_gateways = [
        "https://api.allorigins.win/get?url=",
        "https://api.codetabs.com/v1/proxy/?quest="
    ]

    for url in urls:
        success = False
        # نجربوا البروكسيات بالواحد لين يفتح الموقع
        for gateway in proxy_gateways:
            try:
                proxy_url = f"{gateway}{url}"
                response = requests.get(proxy_url, timeout=30)
                
                if response.status_code == 200:
                    html_content = response.text.lower()
                    
                    found_any = False
                    for movie in target_movies:
                        if movie in html_content:
                            send_telegram_message(f"🚨 تنبيه: تم رصد صفحة لفيلم {movie}! \nالمصدر: {url}")
                            found_any = True
                    
                    if not found_any:
                        print(f"تم فحص {url} بنجاح عبر الوسيط - لا توجد تذاكر.")
                    
                    success = True
                    break # نجح الفحص، ننتقل للرابط اللي بعده
            except:
                continue
        
        if not success:
            print(f"فشل الوصول للرابط {url} حتى عبر الوسائط.")

if __name__ == "__main__":
    check_tickets()
