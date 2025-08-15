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
