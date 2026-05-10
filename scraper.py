import os
import asyncio
from playwright.async_api import async_playwright
import requests

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload)
    except:
        print("Error sending telegram")

async def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    target_movies = ["dune", "backrooms", "odyssey", "mortal kombat", "spider-man"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # إعدادات متصفح أكثر مرونة
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"جاري محاولة فتح الموقع...")
            # غيرنا الانتظار ليكون domcontentloaded (أسرع وأضمن للـ Timeout)
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # نعطوه 10 ثواني "ثابتة" يحمل فيها المحتوى براحته
            await page.wait_for_timeout(10000)
            
            content = await page.content()
            content = content.lower()

            found_any = False
            for movie in target_movies:
                if movie in content:
                    send_telegram_message(f"🚨 لقيت التذاكر! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                    print(f"🎯 صيد ناجح: {movie}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص تم بنجاح: الأفلام المطلوبة مزال ما طلعتش.")
                if "marmara" in content:
                    print("🔍 تأكيد: البوت دخل للموقع وقرأ البيانات صح.")

        except Exception as e:
            print(f"⚠️ حدث خطأ أثناء التحميل: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
