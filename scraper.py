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
        print("خطأ في إرسال التليجرام")

async def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    
    # القائمة المحدثة (ضفنا michael)
    target_movies = [
        "dune", "backrooms", "odyssey", 
        "mortal kombat", "spider-man", "michael"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # إعدادات المتصفح لضمان أفضل توافق مع الموقع
        context = await browser.new_context(
            locale="tr-TR", 
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = await context.new_page()
        
        print(f"جاري فحص الأفلام في Marmara Forum...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # انتظار إضافي بسيط للتأكد من تحميل كل العناصر
        await page.wait_for_timeout(5000)
        
        content = await page.content()
        content = content.lower()

        found_any = False
        for movie in target_movies:
            if movie in content:
                # إرسال التنبيه
                send_telegram_message(f"🚨 تنبيه جديد: تم رصد فيلم {movie.upper()} في Marmara Forum! \nالرابط: {url}")
                print(f"🎯 لقى الفيلم: {movie}")
                found_any = True
        
        if not found_any:
            print("🏁 الفحص تم: لم تظهر أفلام جديدة في القائمة حالياً.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
