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
  url = "https://www.pathe.tn/en/films/dune-troisieme-partie-55711"

  async with async_playwright() as p:
    browser = await p.chromium.launch(headless=True)
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
    )
    page = await context.new_page()

    try:
      print("🔍 بدء الفحص لصفحة فيلم Dune في باثي تونس...")
      await page.goto(url, wait_until="domcontentloaded", timeout=180000)

      # الانتظار قليلاً لضمان استقرار محتوى الصفحة بالكامل
      await page.wait_for_timeout(8000)

      content = await page.content()
      content_lower = content.lower()

      # 1. صمام أمان: التأكد أننا في صفحة الفيلم الحقيقية وليست صفحة خطأ أو فارغة
      if "dune" not in content_lower or "pathe" not in content_lower:
        print(
            "⚠️ تنبيه: الصفحة الحالية لا تبدو كصفحة الفيلم المطلوبة، سنحاول لاحقاً."
        )
        return

      # 2. الجملة المستهدفة للبحث
      not_showing_phrase = "this movie is not yet showing in cinemas"

      # 3. الشرط الحقيقي والمضبوط بدقة
      if not_showing_phrase in content_lower:
        print(
            "⏳ الفيلم ما زال غير متاح للحجز (جملة عدم العرض موجودة ومؤكدة)."
        )
      else:
        # إذا اختفت الجملة حقاً، يتم إرسال التنبيه الحقيقي
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
