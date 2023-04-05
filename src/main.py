import datetime
import logging
import os
import random
import re
import threading
import time

import requests
import schedule
import telebot
from decouple import config
from dotenv import load_dotenv, find_dotenv

from src import where_are_yura_calculation

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

KAL_TEAM_ID = config('KAL_TEAM_ID', default='')
PLATFORM_TOILET_ID = config('PLATFORM_TOILET_ID', default='')
API_KEY = config('OPENAI_TOKEN', default='')
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
BOT_ID = bot.get_me().id
MODEL = "text-davinci-003"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     '<b>дарова ребята =)</b> я очень МОЩНЫЙ хайлоад разработчик любитель мемов покидать',
                     parse_mode='html')


@bot.message_handler(commands=['mvp'])
def start(message):
    bot.send_message(message.chat.id,
                     'сами в своем говне ковыряйтесь я пойду нормальную платформу делать',
                     parse_mode='html')


@bot.message_handler(commands=['govbar'])
def go_v_bar(message):
    # отправляем GET-запрос на сервер OSM
    url = "https://nominatim.openstreetmap.org/search.php"
    params = {"q": "бары у метро чистые пруды", "format": "jsonv2"}
    response = requests.get(url, params=params)
    # извлекаем названия баров из списка результатов
    bars = [r["display_name"] for r in response.json()]
    # выводим случайное название бара
    bot.send_message(message.chat.id, 'МАКСИМАЛНО зову в этот бар: ' + random.choice(bars))


@bot.message_handler(commands=['whereareyura'])
def where_are_yura_reply(message):
    bot.send_message(message.chat.id, where_are_yura_calculation.where_are_yura())


def is_target_message(message):
    if message.chat.type == 'private':
        return True
    if re.search(fr'\B@{bot.get_me().username}\b', message.text):
        return True
    if message.reply_to_message and message.reply_to_message.from_user.id == BOT_ID:
        return True
    return False


@bot.message_handler(func=is_target_message)
def text_reply(message):
    bot.send_message(message.chat.id, f'<i>ваяяя</i> шеф, извиняй, опенаи не прикрутил костян пока, это только MVP', parse_mode='html')


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'document', 'location', 'contact'], func=lambda
        message: message.reply_to_message is not None or message.entities is not None or message.chat.type == 'private')
def media_reply(message):
    bot.send_message(message.chat.id, 'бро я текст ФТ с трудом понимаю зачем ты так сложно', parse_mode='html')


@bot.message_handler(content_types=['video'], func=lambda
        message: message.reply_to_message is not None or message.entities is not None or message.chat.type == 'private')
def video_reply(message):
    bot.send_message(message.chat.id, 'видос бомба бро!!', parse_mode='html')


@bot.message_handler(content_types=['sticker'], func=lambda
        message: message.reply_to_message is not None or message.entities is not None or message.chat.type == 'private')
def sticker_reply(message):
    bot.send_message(message.chat.id, 'бро зачотный стикер =)', parse_mode='html')


def leave_work_notification():
    bot.send_message(KAL_TEAM_ID, 'пасаны не забудьте уйти с работы =) срочно приступить к кайфулям!',
                     parse_mode='html')


if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.polling(none_stop=True)

schedule.every().day.at("18:00").do(leave_work_notification)


# функция для запуска leave_work_notification() в отдельном потоке
def leave_work_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


# запуск leave_work_notification() в отдельном потоке
threading.Thread(target=leave_work_notification).start()

bot.polling(none_stop=True)
