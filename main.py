from telethon import TelegramClient, events

# ضع API ID و API HASH الخاصة بك من my.telegram.org
api_id = 123456      # استبدلها بـ API ID
api_hash = "ضع_API_HASH_هنا"

# إنشاء جلسة باسم "my_account"
client = TelegramClient("my_account", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    name = sender.first_name
    text = event.raw_text
    print(f"📩 رسالة جديدة من {name}: {text}")
    
    # الرد التلقائي
    await event.reply("👋 أهلاً! أنا بوت شخصي شغال بـ Telethon.")

print("🚀 جاري تشغيل البوت...")
client.start()
client.run_until_disconnected()
print("مرحبا! البوت يعمل بنجاح 🎯")
import os
import time
import requests
from datetime import datetime

# قراءة القيم من Secrets
WALLET_ADDRESS = os.environ.get("WALLET_ADDRESS")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
SOLSNIFFER_API_KEY = os.environ.get("SOLSNIFFER_API_KEY")

# إعدادات التداول
BUY_AMOUNT_SOL = 1
SLIPPAGE = 0.15  # 15%
TAKE_PROFIT_MULTIPLIER = 10
HOLD_PROFIT_PERCENT = 0.15

# مصادر العملات
SOURCES = [
    "https://pump.fun/api/board",
    "https://meteora.ag/api/tokens",
    "https://letsbonk.fun/api/tokens"
]

# فحص حساب X (Twitter)
def check_x_account(twitter_handle):
    # هذه دالة شكلية - تحتاج API من Twitter أو scraping
    # هنا سنضع قيم وهمية للاختبار
    followers_count = 5000
    high_profile_followers = True
    username_changes = 2
    return followers_count, high_profile_followers, username_changes

# فحص SolSniffer
def check_solsniffer(contract_address):
    url = f"https://api.solsniffer.com/audit/{contract_address}"
    headers = {"Authorization": f"Bearer {SOLSNIFFER_API_KEY}"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("score", 0)
        else:
            return 0
    except Exception as e:
        print(f"[SolSniffer Error] {e}")
        return 0

# كشف التداول الوهمي (مثال مبسط)
def detect_wash_trading(token_data):
    # إذا كان حجم التداول كبير بشكل غير منطقي في وقت قصير
    volume = token_data.get("volume", 0)
    tx_count = token_data.get("transactions", 0)
    if tx_count > 0 and volume / tx_count > 1000:
        return True
    return False

# تنفيذ شراء
def execute_buy(token):
    print(f"[BUY] شراء {BUY_AMOUNT_SOL} SOL من {token['symbol']} بسعر {token['price']} (انزلاق {SLIPPAGE*100}%)")

# تنفيذ بيع
def execute_sell(token, entry_price):
    print(f"[SELL] بيع {token['symbol']} بسعر {token['price']} (جني أرباح {TAKE_PROFIT_MULTIPLIER}x مع احتفاظ {HOLD_PROFIT_PERCENT*100}%)")

# جلب العملات من المصادر
def fetch_tokens():
    tokens = []
    for src in SOURCES:
        try:
            resp = requests.get(src, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                # دمج البيانات (هنا نفترض أن كل API يعيد قائمة)
                tokens.extend(data)
        except Exception as e:
            print(f"[Fetch Error] {src} => {e}")
    return tokens

# حلقة الفحص المستمر
def main():
    print("[BOT] بدء تشغيل البوت...")
    portfolio = {}  # لحفظ الأسعار عند الشراء
    while True:
        try:
            print(f"\n[SCAN] بدء الفحص في {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
            tokens = fetch_tokens()
            for token in tokens:
                # فحص حساب X
                followers, high_profile, name_changes = check_x_account(token.get("twitter", ""))
                if not high_profile or name_changes > 3:
                    continue

                # فحص SolSniffer
                score = check_solsniffer(token.get("contract", ""))
                if score < 85:
                    continue

                # كشف التداول الوهمي
                if detect_wash_trading(token):
                    continue

                # تنفيذ شراء إذا لم يكن في المحفظة
                if token["symbol"] not in portfolio:
                    execute_buy(token)
                    portfolio[token["symbol"]] = token["price"]
                else:
                    entry_price = portfolio[token["symbol"]]
                    if token["price"] >= entry_price * TAKE_PROFIT_MULTIPLIER:
                        execute_sell(token, entry_price)
                        del portfolio[token["symbol"]]

            time.sleep(60)  # فحص كل دقيقة
        except Exception as e:
            print(f"[ERROR] {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
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
