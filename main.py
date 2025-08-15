import requests
import time
import os

# قراءة API Key و المحفظة من متغيرات البيئة
SOLSNF_API = os.getenv("SOLSNF_API")
WALLET = os.getenv("WALLET")

if not SOLSNF_API or not WALLET:
    raise ValueError("⚠️ تأكد من إضافة SOLSNF_API و WALLET في Secrets على GitHub.")

def check_tokens():
    try:
        url = f"https://api.solsniffer.com/v1/wallet/{WALLET}"
        headers = {"Authorization": f"Bearer {SOLSNF_API}"}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"❌ خطأ: {response.status_code} - {response.text}")
            return
        
        data = response.json()
        
        if not data.get("tokens"):
            print("🚫 لا توجد عملات حالياً.")
            return
        
        print("📊 العملات المكتشفة:")
        for token in data["tokens"]:
            name = token.get("name", "Unknown")
            symbol = token.get("symbol", "")
            price = token.get("price", "N/A")
            print(f"- {name} ({symbol}) | السعر: {price}")
        
    except Exception as e:
        print(f"⚠️ حدث خطأ: {e}")

# تشغيل الفحص كل 60 ثانية
while True:
    check_tokens()
    time.sleep(60)
