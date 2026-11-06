import asyncio
import os
from playwright.async_api import async_playwright
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message}
  try:
    requests.post(url, json=payload)
  except:
    print("خطأ في تيليجرام")


async def check_tickets():
  url = "https://www.pathe.tn/en/films/dune-troisieme-partie-55711"

  async with async_playwright() as p:
    # إطلاق المتصفح مع تمرير بارامترات تمنع الكشف الأمني
    browser = await p.chromium.launch(
        headless=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--window-size=1920,1080",
        ],
    )

    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1920, "height": 1080},
        locale="en-US",
        timezone_id="Africa/Tunis",
    )

    # **الحيلة الأهم:** حذف علامة الأتمتة من المتصفح لخدع نظام الحماية
    await context.add_init_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    page = await context.new_page()

    try:
      print("🔍 بدء الفحص المحصن لصفحة فيلم Dune في باثي تونس...")
      # استخدام وضع العرض العادي مع مهلة أطول واستقرار شبكي
      await page.goto(
          url, wait_until="domcontentloaded", timeout=180000
      )

      # محاكاة سلوك بشري طفيف (حركة عشوائية أو انتظار تفاعلي)
      await page.wait_for_timeout(10000)

      content = await page.content()
      content_lower = content.lower()

      # صمام الأمان المزدوج: التأكد من أن الصفحة حملت المحتوى البشري المطلوب
      if "dune" not in content_lower or "pathe" not in content_lower:
        print(
            "⚠️ تنبيه: لا تزال الحماية تمنع الوصول أو أن الصفحة لم تحمل بالكامل."
        )
        return

      # الجملة المستهدفة للبحث
      not_showing_phrase = "this movie is not yet showing in cinemas"

      if not_showing_phrase in content_lower:
        print(
            "⏳ الفيلم ما زال غير متاح للحجز (جملة عدم العرض موجودة ومؤكدة)."
        )
      else:
        # إذا اختفت الجملة حقاً وبشكل مؤكد
        alert_msg = (
            "🚨 تنبيه عاجل: تم إزالة جملة عدم العرض من صفحة Dune في"
            f" باثي!\nقد يكون الحجز قد فتح الآن 🎟️🔥\nالرابط:\n{url}"
        )
        send_telegram_message(alert_msg)
        print("🎉 تم كشف التغيير الحقيقي وإرسال التنبيه على تيليجرام!")

    except Exception as e:
      print(f"⚠️ حدث خطأ أثناء التصفح: {e}")

    finally:
      await browser.close()


if __name__ == "__main__":
  asyncio.run(check_tickets())
