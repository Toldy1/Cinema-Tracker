import os
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    print(f"جاري محاولة إرسال رسالة لتليجرام...")
    try:
        r = requests.post(url, json=payload)
        print(f"رد تليجرام: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"خطأ في إرسال تليجرام: {e}")

def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    # جرب إضافة كلمة "marmara" للتأكد 100%
    target_movies = ["marmara", "cinema", "dune", "backrooms", "the backrooms"]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            html_content = response.text.lower()
            
            # طباعة أول 1000 حرف من الصفحة في السجلات لنرى ماذا يرى البوت
            print("--- بداية عينة الكود المسحوب ---")
            print(html_content[:1000])
            print("--- نهاية عينة الكود المسحوب ---")

            for movie in target_movies:
                if movie in html_content:
                    print(f"🎯 تم العثور على الكلمة: {movie}")
                    send_telegram_message(f"✅ تيست ناجح! البوت لقى كلمة: {movie}")
                else:
                    print(f"❌ لم يجد كلمة: {movie}")
        else:
            print(f"❌ فشل الاتصال بالموقع، كود: {response.status_code}")
    except Exception as e:
        print(f"⚠️ خطأ تقني: {e}")

if __name__ == "__main__":
    check_tickets()
