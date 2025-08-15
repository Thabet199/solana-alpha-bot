import os
import time
import requests

# قراءة المتغيرات من GitHub Secrets
SOLSNF_API = os.getenv("SOLSNIFFER_API_KEY")
WALLET = os.getenv("WALLET_PRIVATE_KEY")

# التأكد من أن المتغيرات موجودة
if not SOLSNF_API or not WALLET:
    raise ValueError("⚠️ تأكد من إضافة SOLSNIFFER_API_KEY و WALLET_PRIVATE_KEY في Secrets على GitHub.")

# رابط API لفحص العملات
API_URL = "https://api.solsniffer.com/v1/tokens"

def check_new_tokens():
    try:
        headers = {"Authorization": f"Bearer {SOLSNF_API}"}
        response = requests.get(API_URL, headers=headers, timeout=10)

        if response.status_code == 200:
            tokens = response.json()
            print(f"✅ تم جلب {len(tokens)} عملة جديدة.")
            for token in tokens:
                print(f"- {token.get('symbol', 'N/A')} | {token.get('address', 'N/A')}")
        else:
            print(f"❌ خطأ في جلب البيانات: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"⚠️ حدث خطأ: {e}")

if __name__ == "__main__":
    print("🚀 بدء فحص العملات الجديدة كل ثانية...")
    while True:
        check_new_tokens()
        time.sleep(1)  # فحص كل ثانية
