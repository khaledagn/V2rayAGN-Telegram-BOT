from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests
import os

API_URL = "https://www.khaledagn.me:8443"
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@khaledagn")  
BOT_COPYRIGHT = "\u00A9 2024 KhaledAGN V2Ray Config Bot"  



TEMP_CONFIGS = {}

def register_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start_handler(message: Message):
        """
        Handle the /start command.
        """
        print(f"Received /start from user: {message.chat.id}")
        try:
            user_id = message.chat.id
           
            if is_user_subscribed(bot, user_id):
                send_welcome_message(bot, message)
            else:
                send_subscription_prompt(bot, message)
        except Exception as e:
            print(f"Error in /start handler: {e}")
            bot.reply_to(message, "\U0000274C An error occurred. Please try again later.")

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query_handler(call: CallbackQuery):
        """
        Handle button interactions.
        """
        print(f"Callback data: {call.data} from user: {call.from_user.id}")
        try:
            if call.data == "menu":
                send_config_menu(bot, call)
            elif call.data == "info":
                send_bot_info(bot, call)
            elif call.data == "exit":
                send_exit_message(bot, call)
            elif call.data == "start":
                send_welcome_message(bot, call.message)
            elif call.data.startswith("copy_"):
                config_index = int(call.data.replace("copy_", ""))
                send_copied_message(bot, call, TEMP_CONFIGS.get(config_index, ""))
            elif call.data == "back":
                send_welcome_message(bot, call.message)
            else:
                send_configs(bot, call)
        except Exception as e:
            print(f"Error handling callback query: {e}")
            bot.send_message(call.message.chat.id, "\U0000274C An error occurred while processing your request.")

def send_config_menu(bot, call):
    """
    Display the V2Ray configuration types menu.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("\U0001F680 VMess", callback_data="vmess"),
        InlineKeyboardButton("\U0001F6E1 VLESS", callback_data="vless"),
    )
    keyboard.add(
        InlineKeyboardButton("\U0001F512 Trojan", callback_data="trojan"),
        InlineKeyboardButton("\U0001F310 Shadowsocks (SS)", callback_data="ss"),
    )
    keyboard.add(
        InlineKeyboardButton("\U0001F310 ShadowsocksR (SSR)", callback_data="ssr"),
        InlineKeyboardButton("\U0001F4E1 TUIC", callback_data="tuic"),
    )
    keyboard.add(InlineKeyboardButton("\U00002B05 Back", callback_data="back"))

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="\U0001F50D *Select the configuration type* you want to retrieve:\n\n",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

def send_subscription_prompt(bot, message):
    """
    Prompt the user to subscribe to the channel.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("\U0001F517 Subscribe", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}"))
    bot.reply_to(
        message,
        "\U0001F44B Please subscribe to the channel to access V2Ray configs.\n"
        "Once subscribed, type /start again.",
        reply_markup=keyboard,
    )

def send_welcome_message(bot, message):
    """
    Send a beautiful welcome message with options.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("\U0001F310 Get V2Ray Configs", callback_data="menu"),
        InlineKeyboardButton("\U00002139 About This Bot", callback_data="info"),
    )
    keyboard.add(InlineKeyboardButton("\U0000274C Exit", callback_data="exit"))
    bot.reply_to(
        message,
        "\U0001F44B Welcome to the *KhaledAGN V2Ray Config Bot*! \U0001F389\n\n"
        "\U0001F31F Use this bot to fetch organized and reliable V2Ray configurations.\n"
        "\U0001F4CC Make your selections below to get started.\n\n"
        f"{BOT_COPYRIGHT}",
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

def send_configs(bot, call):
    """
    Fetch and display configurations based on the user's selection.
    """
    config_type = call.data
    try:
        response = requests.get(f"{API_URL}/configs/{config_type}?limit=5")
        if response.status_code == 200:
            data = response.json()
            configs = data.get("configs", [])[:5]   

            
            TEMP_CONFIGS.clear()
            for i, config in enumerate(configs):
                TEMP_CONFIGS[i] = config

            keyboard = InlineKeyboardMarkup()
            for i in range(len(configs)):
                keyboard.add(InlineKeyboardButton(f"Copy Config {i+1}", callback_data=f"copy_{i}"))
            keyboard.add(InlineKeyboardButton("\U00002B05 Back", callback_data="menu"))

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"\U0001F4CB *{config_type.upper()} Configurations*\n\nClick a button below to copy the configuration.\n\n",
                reply_markup=keyboard,
                parse_mode="Markdown",
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"\U0000274C Unable to fetch {config_type.upper()} configurations. Please try again later.",
            )
    except Exception as e:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="\U0000274C An error occurred while fetching configurations. Please try again later.",
        )
        print(f"Error fetching configs: {e}")

def send_copied_message(bot, call, config_text):
    """
    Send the configuration text to the user for copying.
    """
    if config_text:
        bot.send_message(
            chat_id=call.message.chat.id,
            text=f"\U0001F4CC *Click to copy Configuration*:\n\n`{config_text}`\n\n"
            f"{BOT_COPYRIGHT}",
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            chat_id=call.message.chat.id,
            text="\U0000274C No configuration available to copy.",
        )

def is_user_subscribed(bot, user_id):
    """
    Check if a user is subscribed to the channel.
    """
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False

def send_exit_message(bot, call):
    """
    Send an exit message with a Start Again button to return to the main menu.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("\U0001F503 Start Again", callback_data="start"))   

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="\U0001F44B Thank you for using the bot. See you next time! \U0001F60A\n\n"
             "Click the button below to start again.",
        reply_markup=keyboard,   
    )

def send_bot_info(bot, call):
    """
    Send bot information with a back button.
    """
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("\U00002B05 Back", callback_data="start"))   

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=(
            "\U00002139 *About This Bot*\n\n"
            "This bot provides V2Ray configurations, helping you manage your proxies easily.\n\n"
            "\U0001F4A1 *Features:*\n"
            "- Organized configuration options\n"
            "- Easy-to-use interface\n"
            "- Reliable and updated configurations\n\n"
            "\U0001F527 *Developed by:* Khaled AGN\n\n"
            "\U0001F4E2 *Follow Khaled AGN on Social Media:*\n"
            "[\U0001F426 Twitter](https://twitter.com/khaled_agn)\n"
            "[\U0001F4F1 Telegram Channel](https://t.me/khaledagn)\n"
            "[\U0001F310 Website](https://www.khaledagn.me)\n"
            "[\U0001F3AC Instagram](https://www.instagram.com/khaledagn)\n"
            "[\U0001F4FA YouTube](https://youtube.com/c/KhaledAGN)\n\n"
            f"{BOT_COPYRIGHT}"
        ),
        reply_markup=keyboard,
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )

