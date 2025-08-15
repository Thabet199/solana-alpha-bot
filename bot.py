from telethon import TelegramClient, events

api_id = 27083294
api_hash = '2fee98fb465d41ad711bdf39dc40ed37'
bot_token = '8218369326:AAEDMBpc4DvB6J6CbfEewtU3VTOoTeiV-FU'

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage)
async def handler(event):
    await event.respond("✅ Bot is working!")

print("🚀 Bot started!")
bot.run_until_disconnected()

