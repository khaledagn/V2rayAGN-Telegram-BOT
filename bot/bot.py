from bot import get_bot_updater
from bot.handlers import start, send_configs
from telegram.ext import CommandHandler, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN", "7798305127:AAGmK30Uwk8O1ES9lvGOXghWoYm03Cd0lrI") 

def main():
    updater = get_bot_updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

  
    dispatcher.add_handler(CommandHandler("start", start))

 
    dispatcher.add_handler(CallbackQueryHandler(send_configs))

    print("Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
