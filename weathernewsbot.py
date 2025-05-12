import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import nest_asyncio
import asyncio

BOT_TOKEN = 'توکن_ربات_تو_اینجا'  # توکن ربات خودت رو اینجا وارد کن
API_KEY = 'کلید_آب_و_هوا_تو_اینجا'  # کلید API خودت رو اینجا وارد کن

nest_asyncio.apply()

# دیکشنری برای نام استان‌ها و شهرها
provinces = {
    'تهران': ['تهران', 'شمیرانات', 'ری'],
    'مازندران': ['ساری', 'نوشهر', 'بابل'],
    # سایر استان‌ها رو هم می‌تونی به همین شکل اضافه کنی
}

# فانکشن دریافت اطلاعات هواشناسی
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

# فانکشن برای خوشامدگویی و درخواست نام شهر
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ارسال پیام خوشامدگویی
    welcome_message = (
        "سلام! من ربات هواشناسی هستم. لطفاً نام شهر یا استان خود را وارد کنید. "
        "مثلاً: تهران، مازندران، یا بابل."
    )
    await update.message.reply_text(welcome_message)

    # دریافت پیام کاربر (شهر یا استان)
    city_or_province = update.message.text.strip()

    # بررسی استان‌ها
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
