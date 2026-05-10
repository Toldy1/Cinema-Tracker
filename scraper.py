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
    # قائمة الأهداف
    target_movies = ["dune", "backrooms", "odyssey", "mortal kombat", "spider-man"]

    async with async_playwright() as p:
        # تشغيل المتصفح بوضعية التخفي
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        print(f"جاري فتح موقع Marmara Forum...")
        # الانتظار حتى استقرار الشبكة لضمان تحميل الصور والبوسترات
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # قراءة المحتوى بالكامل
        content = await page.content()
        content = content.lower()

        found_any = False
        for movie in target_movies:
            if movie in content:
                send_telegram_message(f"🚨 لقيت التذاكر! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                print(f"🎯 صيد ناجح: {movie}")
                found_any = True
        
        if not found_any:
            print("🏁 الفحص تم: الأفلام المطلوبة مزال ما طلعتش في المتصفح.")
            # تأكيد إننا في الصفحة الصح
            if "marmara" in content:
                print("🔍 البوت حالياً داخل صفحة مارمارا فوروم بنجاح.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
