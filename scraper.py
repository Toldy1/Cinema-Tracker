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
    # ضفنا مسارات خريطة الموقع (sitemap.xml) لأن الحماية عليها ضعيفة
    urls = [
        "https://www.biletiva.com/sitemap.xml",
        "https://www.biletiva.com/tags/events?cat=sinema",
        "https://worldcinezone.com.tr/marmaraforum"
    ]
    
    # أسماء الأفلام بحروف صغيرة عشان المطابقة
    target_movies = ["dune", "spider-man", "doomsday", "odyssey"]

    # التنكر على هيئة عنكبوت جوجل للعبور من الحماية
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                html_content = response.text.lower()
                
                found_any = False
                for movie in target_movies:
                    # لو اسم الفيلم انضاف في خريطة الموقع أو الصفحة
                    if movie in html_content:
                        send_telegram_message(f"🚨 تنبيه اختراق: تم رصد صفحة لفيلم {movie}! \nالمصدر: {url}")
                        found_any = True
                        
                if not found_any:
                    print(f"تم فحص {url} بنجاح (عبر ثغرة Googlebot) - لا توجد تذاكر حالياً.")
            else:
                # لو صدنا، مش حنبعت رسالة لتليجرام عشان ما نزعجكش، بنكتفي بطباعة الخطأ في السجلات
                print(f"تم صد الهجوم التنكري على {url} بكود {response.status_code}")

        except Exception as e:
            print(f"خطأ في الاتصال مع {url}: {e}")

if __name__ == "__main__":
    check_tickets()
