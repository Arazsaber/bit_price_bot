from telegram import Bot
from telegram.ext import ApplicationBuilder, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests
import logging

TOKEN = "8052658426:AAFDSXMIhzLH40RY1zGC0DVHHytaj5W6_Zs"
CHANNEL_ID = "-1001234567890"  # آی‌دی عددی کانال تلگرام
INTERVAL_MINUTES = 1           # فاصله ارسال خودکار (دقیقه)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ---- دریافت قیمت بیت‌کوین ----
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data["bitcoin"]["usd"]

# ---- ارسال پیام به کانال ----
async def send_price_to_channel(bot: Bot):
    try:
        price = get_bitcoin_price()
        text = f"💰 قیمت لحظه‌ای بیت‌کوین: ${price}"
        await bot.send_message(chat_id=CHANNEL_ID, text=text)
        logging.info("✅ پیام ارسال شد")
    except Exception as e:
        logging.error(f"❌ خطا در ارسال پیام: {e}")


# تابع برای دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دیدن قیمت بیت‌کوین دستور /price رو بزن.")

# تابع برای دستور /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price = get_bitcoin_price()
        await update.message.reply_text(f"💰 قیمت لحظه‌ای بیت‌کوین: ${price}")
    except Exception as e:
        await update.message.reply_text("❌ خطا در دریافت قیمت بیت‌کوین.")

# تابع اصلی اجرا
async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    bot = Bot(token=TOKEN)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_price_to_channel, "interval", minutes=INTERVAL_MINUTES, args=[bot])
    scheduler.start()

    print("🤖 ربات فعال شد و هر ۵ دقیقه قیمت رو در کانال می‌فرسته.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
