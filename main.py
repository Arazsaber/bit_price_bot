from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8052658426:AAFDSXMIhzLH40RY1zGC0DVHHytaj5W6_Zs"  # جای YOUR_BOT_TOKEN را با توکن ربات خود جایگزین کنید

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! به ربات من خوش آمدید!')

def echo(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    update.message.reply_text(f'شما گفتید: {user_message}')

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()