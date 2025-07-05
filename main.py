from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

TOKEN = "8052658426:AAFDSXMIhzLH40RY1zGC0DVHHytaj5W6_Zs"

# تابع دریافت قیمت بیت‌کوین از CoinGecko API
def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = data["bitcoin"]["usd"]
    return price

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
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    print("✅ ربات فعال شد.")
    app.run_polling()

if __name__ == "__main__":
    main()
