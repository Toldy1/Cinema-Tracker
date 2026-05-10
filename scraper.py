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
        print("خطأ في تليجرام")

async def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    
    # القائمة الكاملة والنهائية (مع إضافة doomsday)
    target_movies = [
        "dune", "backrooms", "the backrooms", "odyssey", "spider-man", "spiderman", "doomsday"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        try:
            print(f"بدء الفحص بصبر طويل (3 دقائق)...")
            # الانتظار حتى تحميل الصفحة بالكامل
            await page.goto(url, wait_until="load", timeout=180000)
            
            # النزول لأسفل الصفحة لضمان تحميل كل الأفلام الديناميكية
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(10000) # استراحة 10 ثواني للتحميل الكامل
            
            content = await page.content()
            content = content.lower()

            found_any = False
            for movie in target_movies:
                if movie in content:
                    send_telegram_message(f"🚨 صيد جديد! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                    print(f"🎯 تم العثور على: {movie}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص انتهى: الأفلام المطلوبة مزال ما نزلتش.")

        except Exception as e:
            print(f"⚠️ الموقع علّق المرة هذه (Timeout). حيجرب تلقائياً بعد نص ساعة. الخطأ: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
