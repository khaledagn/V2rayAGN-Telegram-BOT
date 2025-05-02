import telebot
from bot.handlers import register_handlers
import os


BOT_TOKEN = os.getenv("BOT_TOKEN", "7798305127:AAGmK30Uwk8O1ES9lvGOXghWoYm03Cd0lrI") 

WEBHOOK_URL = os.getenv("WEBHOOK", "https://www.khaledagn.me:8443") 

bot = telebot.TeleBot(BOT_TOKEN)

def setup_webhook():
    """
    Set up the webhook for the bot.
    """
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    print(f"Webhook set to {WEBHOOK_URL}")

register_handlers(bot)
