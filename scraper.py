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
    # تحسين الـ User-Agent لتجنب الحظر
    context = await browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    )
    page = await context.new_page()

    try:
      print("🔍 بدء الفحص لصفحة فيلم Dune في باثي تونس...")
      await page.goto(url, wait_until="load", timeout=180000)

      # 1. طباعة عنوان الصفحة للتأكد هل تم فتحها أم حظرنا؟
      page_title = await page.title()
      print(f"📌 عنوان الصفحة الحالي: {page_title}")

      # النزول لأسفل الصفحة لضمان تحميل المحتوى بالكامل
      await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
      await page.wait_for_timeout(8000)

      content = await page.content()
      content_lower = content.lower()

      # 2. طباعة عينة من محتوى الصفحة في السجلات لنرى ماذا قرأ السيرفر
      print(
          "📄 عينة من محتوى الصفحة (أول 350 حرف):"
          f" {content_lower[:350]}..."
      )

      # فحص الحظر الأمني
      if "just a moment" in content_lower or "access denied" in content_lower:
        print("⚠️ تنبيه: نظام حماية الموقع (Cloudflare) قام بحظر السيرفر!")
        return

      # العبارة المستهدفة
      not_showing_phrase = "this movie is not yet showing in cinemas"

      # الشرط: هل العبارة غير موجودة؟
      if not_showing_phrase not in content_lower:
        alert_msg = (
            "🚨 تنبيه عاجل: تم إزالة جملة عدم العرض من صفحة Dune في"
            f" باثي!\nقد يكون الحجز قد فتح الآن 🎟️🔥\nالرابط:\n{url}"
        )
        # لتجنب إزعاجك في الاختبارات القادمة اذا كانت العبارة موجودة فعلاً:
        # سنقوم بإرسال التنبيه فقط إذا متأكدين، لكن اترك هذا الشرط الآن لنرى السجلات
        send_telegram_message(alert_msg)
        print("🎉 تم كشف تغيير في الصفحة وإرسال التنبيه على تيليجرام!")
      else:
        print(
            "⏳ الفيلم ما زال غير متاح للحجز (جملة عدم العرض لا تزال موجودة في"
            " الصفحة بصورة سليمة)."
        )

    except Exception as e:
      print(f"⚠️ حدث خطأ أثناء التصفح: {e}")

    finally:
      await browser.close()


if __name__ == "__main__":
  asyncio.run(check_tickets())
