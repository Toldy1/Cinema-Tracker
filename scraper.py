import os
import requests

# جلب البيانات من الإعدادات السرية في GitHub
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
    # ركزنا هنا على الرابط اللي يفتح معاك بنجاح
    url = "https://worldcinezone.com.tr/marmaraforum"
    
    # قائمة الأفلام بكل الاحتمالات (سمول لتر)
    target_movies = ["dune", "spider-man", "spiderman", "doomsday", "odyssey"]
    
    # هيدرز بسيطة عشان نبانوا كأننا متصفح عادي
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        print(f"بدء فحص سينما Marmara Forum...")
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            html_content = response.text.lower()
            
            found_any = False
            for movie in target_movies:
                if movie in html_content:
                    send_telegram_message(f"🚨 عاااجل: تذاكر فيلم {movie} نزلت في Marmara Forum! \nالرابط: {url}")
                    print(f"لقيت الفيلم: {movie}")
                    found_any = True
            
            if not found_any:
                print("الفحص تم بنجاح: الفيلم مزال ما نزلش في القائمة.")
        else:
            print(f"فشل الوصول للموقع، كود الحالة: {response.status_code}")

    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")

if __name__ == "__main__":
    check_tickets()
