import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import nest_asyncio
import asyncio

BOT_TOKEN = '8168815492:AAEno67sEO7xNLCSJ8IE6gx104CACEmr3IY'

API_KEY = 'ce668425dd9087eb91cb4fb974ef3ca9'

nest_asyncio.apply()

async def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en"
        response = requests.get(url)
        data = response.json()
        if data.get('main'):
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            return f"Temperature in {city}: {temp}°C\nCondition: {description}"
        else:
            return "City not found. Please try again."
    except Exception as e:
        return f"Error retrieving data: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.strip()
    result = await get_weather(city)
    await update.message.reply_text(result)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())