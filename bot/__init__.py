from telegram.ext import Updater

def get_bot_updater(token):
    return Updater(token=token, use_context=True)
