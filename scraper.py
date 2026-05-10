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
        print("Error sending message")

async def check_tickets():
    url = "https://worldcinezone.com.tr/marmaraforum"
    target_movies = ["dune", "backrooms", "odyssey", "mortal kombat", "spider-man"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # إعدادات إضافية لتسريع التحميل وتجنب التعليق
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()
        
        print(f"جاري محاولة فتح الموقع...")
        try:
            # التغيير الجوهري هنا: استعملنا domcontentloaded بدل networkidle
            await page.goto(url, wait_until="domcontentloaded", timeout=45000)
            
            # نعطوه 10 ثواني "صافية" عشان الـ JavaScript يعرض الأفلام
            print("وصلنا للكود الأساسي، ننتظر تحميل الأفلام...")
            await page.wait_for_timeout(10000) 
            
            content = await page.content()
            content = content.lower()

            found_any = False
            for movie in target_movies:
                if movie in content:
                    send_telegram_message(f"🚨 صيد ثمين! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                    print(f"🎯 لقى الفيلم: {movie}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص تم: لم يتم العثور على الأفلام المطلوبة حالياً.")
                if "marmara" in content:
                    print("✅ تأكيد: البوت داخل الصفحة بنجاح وقرأ المحتوى.")

        except Exception as e:
            print(f"⚠️ حدث خطأ أو تأخير: {e}")
            # حتى لو صار تأخير، نحاولوا نقرأ اللي وصل من الصفحة
            content = await page.content()
            if any(movie in content.lower() for movie in target_movies):
                 print("🎯 لقى الفيلم حتى مع وجود خطأ في التحميل!")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
