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
        # استخدام User Agent حقيقي لتفادي أي حظر
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            print(f"جاري فتح الموقع...")
            # التعديل هنا: الانتظار حتى تحميل الـ DOM فقط لتجنب الـ Timeout
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # انتظار يدوي لمدة 10 ثواني لضمان ظهور أسماء الأفلام الديناميكية
            print("الانتظار لظهور محتوى الأفلام...")
            await page.wait_for_timeout(10000)
            
            content = await page.content()
            content = content.lower()

            found_any = False
            for movie in target_movies:
                if movie in content:
                    send_telegram_message(f"🚨 صيد ناجح! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                    print(f"🎯 تم العثور على: {movie}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص تم: الأفلام المطلوبة مزال ما طلعتش.")
                if "marmara" in content:
                    print("🔍 تأكيد: البوت قرأ محتوى الصفحة بنجاح.")
        
        except Exception as e:
            print(f"⚠️ حدث خطأ أثناء الفحص: {e}")
        
        finally:
            await browser.close()

if name == "__main__":
    asyncio.run(check_tickets())
