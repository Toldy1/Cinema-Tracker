import os
from bs4 import BeautifulSoup
from curl_cffi import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")


def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message}
  try:
    requests.post(url, json=payload)
  except:
    print("خطأ في تيليجرام")


def check_tickets():
  url = "https://www.pathe.tn/en/films/dune-troisieme-partie-55711"

  print("🔍 بدء الفحص عبر انتحال بصمة المتصفح (curl_cffi)...")

  try:
    # استخدام curl_cffi لانتحال متصفح Chrome الحقيقي وتجاوز Cloudflare
    response = requests.get(url, impersonate="chrome120", timeout=30)

    print(f"📌 كود الاستجابة من الموقع: {response.status_code}")

    if response.status_code != 200:
      print(f"⚠️ الموقع رفض الطلب أو أعطى كود خطأ: {response.status_code}")
      return

    html_content = response.text
    content_lower = html_content.lower()

    # صمام الأمان: التأكد من أننا وصلنا لصفحة الفيلم الصحيحة
    if "dune" not in content_lower or "pathe" not in content_lower:
      print(
          "⚠️ تنبيه: المحتوى المستقبل لا يطابق صفحة الفيلم المطلوبة (قد يكون حظر"
          " أو إعادة توجيه)."
      )
      return

    # الجملة المستهدفة للبحث
    not_showing_phrase = "t5hebud538hdbiest"

    if not_showing_phrase in content_lower:
      print("⏳ الفيلم ما زال غير متاح للحجز (جملة عدم العرض موجودة ومؤكدة).")
    else:
      alert_msg = (
          "🚨 تنبيه عاجل: تم إزالة جملة عدم العرض من صفحة Dune في باثي!\nقد"
          f" يكون الحجز قد فتح الآن 🎟️🔥\nالرابط:\n{url}"
      )
      send_telegram_message(alert_msg)
      print("🎉 تم كشف التغيير الحقيقي وإرسال التنبيه على تيليجرام!")

  except Exception as e:
    print(f"⚠️ حدث خطأ أثناء الاتصال: {e}")


if __name__ == "__main__":
  check_tickets()
