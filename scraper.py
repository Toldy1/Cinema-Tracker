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
    
    # القائمة المحدثة (ضفنا Michael)
    target_movies = [
        "dune", "backrooms", "the backrooms", 
        "odyssey", "mortal kombat", "spider-man", 
        "spiderman", "michael"
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        print(f"جاري فحص الموقع...")
        await page.goto(url, wait_until="networkidle", timeout=60000)
        
        # نزيدوا وقت الانتظار لـ 7 ثواني عشان نضمن إن كل البوسترات (بما فيها مايكل) تحملت
        await page.wait_for_timeout(7000)
        
        content = await page.content()
        content = content.lower()

        found_any = False
        for movie in target_movies:
            if movie in content:
                send_telegram_message(f"🚨 لقيته! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                print(f"🎯 تم العثور على: {movie}")
                found_any = True
        
        if not found_any:
            print("🏁 الفحص انتهى: الأفلام المطلوبة مزال ما نزلتش.")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
