import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import nest_asyncio
import asyncio

BOT_TOKEN = '8168815492:AAEno67sEO7xNLCSJ8IE6gx104CACEmr3IY'
API_KEY = 'ce668425dd9087eb91cb4fb974ef3ca9'

nest_asyncio.apply()

provinces = {
    'تهران': ['تهران', 'شمیرانات', 'ری'],
    'مازندران': ['ساری', 'نوشهر', 'بابل'],
}

async def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=fa"
        response = requests.get(url)
        data = response.json()
        if data.get('main'):
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description']

            return (
                f"📍 شهر: {city}\n"
                f"🌡 دما: {temp}°C\n"
                f"🤒 حس واقعی: {feels_like}°C\n"
                f"💧 رطوبت: {humidity}%\n"
                f"🌀 باد: {wind_speed} m/s\n"
                f"📈 فشار هوا: {pressure} hPa\n"
                f"🌥 وضعیت: {description}"
            )
        else:
            return "شهر پیدا نشد. لطفاً نام دقیق شهر را وارد کن."
    except Exception as e:
        return f"خطا در دریافت اطلاعات: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = (
        "سلام! من ربات هواشناسی هستم. لطفاً نام شهر یا استان خود را وارد کنید. "
        "مثلاً: تهران، شیراز یا بابل."
    )
    await update.message.reply_text(welcome_message)


    city_or_province = update.message.text.strip()


    found_province = False
    for province, cities in provinces.items():
        if city_or_province in cities:
            found_province = True
            city = city_or_province
            result = await get_weather(city)
            await update.message.reply_text(result)
            break
        elif city_or_province == province:
            found_province = True
            await update.message.reply_text(f"شما استان {province} را وارد کردید، لطفاً یک شهر را وارد کنید.")
            break

    if not found_province:
        result = await get_weather(city_or_province)
        await update.message.reply_text(result)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("ربات در حال اجراست...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
