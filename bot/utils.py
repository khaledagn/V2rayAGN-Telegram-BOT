from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_inline_keyboard(buttons):
    keyboard = [[InlineKeyboardButton(text, callback_data=data)] for text, data in buttons]
    return InlineKeyboardMarkup(keyboard)
