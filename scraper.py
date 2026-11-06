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
    print("خطأ في تلجرام")


async def check_tickets():
  # رابط صفحة فيلم Dune المباشر في باثي تونس
  url = "https://www.pathe.tn/en/films/dune-troisieme-partie-55711"

  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    )
    page = await context.new_page()

    try:
      print("🔍 بدء الفحص لصفحة فيلم Dune في باثي تونس...")
      await page.goto(url, wait_until="load", timeout=180000)

      # النزول لأسفل الصفحة لضمان تحميل المحتوى بالكامل
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
      await page.wait_for_timeout(5000)

      content = await page.content()
      content_lower = content.lower()

      # الجملة الحالية التي تدل على أن الفيلم لم يبدأ عرضه بعد
      not_showing_phrase = "This movie is not yet showing in cinemas"

      # الشرط: إذا اختفت هذه الجملة من الصفحة، فهذا يعني أن الحجز قد فتح!
      if not_showing_phrase not in content_lower:
        alert_msg = (
            "🚨 تنبيه عاجل: تم إزالة جملة (This movie is not yet showing in cinemas) من صفحة Dune في"
            f" باثي!\nقد يكون الحجز قد فتح الآن 🎟️🔥\nالرابط:\n{url}"
        )
        send_telegram_message(alert_msg)
        print("🎉 تم كشف تغيير في الصفحة وإرسال التنبيه على تيليجرام!")
      else:
        print(
            "⏳ الفيلم ما زال غير متاح للحجز (جملة عدم العرض لا تزال موجودة)."
        )

    except Exception as e:
      print(f"⚠️ حدث خطأ أثناء التصفح: {e}")

    finally:
      await browser.close()


if __name__ == "__main__":
  asyncio.run(check_tickets())
