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
        pass

async def check_tickets():
    # الرابط بدون www لأن الـ DNS بتاعهم يرفض فيها أحياناً من سيرفرات أمريكا
    url = "https://worldcinezone.com.tr/marmaraforum"
    target_movies = ["dune", "backrooms", "the backrooms", "odyssey", "mortal kombat", "spider-man", "spiderman"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        try:
            print(f"جاري محاولة فتح: {url}")
            # زدنا الوقت لـ 90 ثانية وغيرنا طريقة الانتظار لـ load عشان نضمن تخطي الـ DNS
            await page.goto(url, wait_until="load", timeout=90000)
            
            # استراحة 5 ثواني عشان مورتال كومبات والبوسترات يلحقوا يطلعوا
            await page.wait_for_timeout(5000)
            
            content = await page.content()
            content = content.lower()

            found_any = False
            for movie in target_movies:
                if movie in content:
                    send_telegram_message(f"🚨 لقيته! فيلم {movie} نزل في Marmara Forum! \nالرابط: {url}")
                    print(f"🎯 لقى: {movie}")
                    found_any = True
            
            if not found_any:
                print("🏁 الفحص انتهى: الأفلام مزال ما طلعتش.")
                
        except Exception as e:
            print(f"❌ خطأ في فتح الرابط: {e}")
            # لو فشل، يبعتلك تنبيه إن السكربت فيه مشكلة تقنية (اختياري)
            # send_telegram_message(f"⚠️ تنبيه تقني: السكربت مش عارف يوصل للموقع.")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(check_tickets())
