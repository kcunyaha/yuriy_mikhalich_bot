import os
import re

import telebot

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
BOT_ID = bot.get_me().id


def is_target_message(message):
    if message.chat.type == 'private':
        return True
    if re.search(fr'\B@{bot.get_me().username}\b', message.text):
        return True
    if message.reply_to_message and message.reply_to_message.from_user.id == BOT_ID:
        return True
    return False
