import logging
import os
import re
import random
import threading
import time
import requests
import datetime
import openai

import schedule
import telebot
from decouple import config
from dotenv import load_dotenv, find_dotenv

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

KAL_TEAM_ID = config('KAL_TEAM_ID', default='')
PLATFORM_TOILET_ID = config('PLATFORM_TOILET_ID', default='')
API_KEY = config('OPENAI_TOKEN', default='')
load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
BOT_ID = bot.get_me().id
MODEL = "text-davinci-003"


def openAI(prompt):
    # Make the request to the OpenAI API
    response = requests.post(
        'https://api.openai.com/v1/completions',
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={'model': MODEL, 'prompt': prompt, 'temperature': 0.4, 'max_tokens': 300}
    )

    result = response.json()
    final_result = ''.join(choice['text'] for choice in result['choices'])
    return final_result


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     '<b>дарова ребята =)</b> я очень МОЩНЫЙ хайлоад разработчик любитель мемов покидать',
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
def where_are_yura(message):
    now = datetime.datetime.now()  # получаем текущее время
    sleep_time = datetime.time(8, 30, 0)
    taxi_morning_time = datetime.time(10, 5, 0)
    working_time = datetime.time(19, 30, 0)
    taxi_evening_time = datetime.time(21, 0, 0)
    if now.time() <= sleep_time:
        bot.send_message(message.chat.id, 'шеф, я сейчас сплю =) напиши попозже всё порешаем все вопросики')
    elif now.time() <= taxi_morning_time:
        bot.send_message(message.chat.id,
                         'началник, МАКСИМАЛНО еду на такси, на дейлик опоздаю на 5 минут, не бей тока')
    elif now.time() <= working_time:
        chance = random.randint(1, 100)
        if chance >= 50:
            bot.send_message(message.chat.id, 'ЧЕГО ТЫ ОПЯТЬ СИДИШЬ РАБОТАЕШЬ, курить пойдем =)')
        else:
            bot.send_message(message.chat.id, 'балин я работаю МОЩНО, ничего не успеваю =(')
    elif now.time() <= taxi_evening_time:
        bot.send_message(message.chat.id, 'бро, я уже домой еду, давай завтра поправлю все баги и выкачу')
    else:
        bot.send_message(message.chat.id, 'ваяяя я тут МОЩНО сижу дома кайфую =)')


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
    bot.send_message(message.chat.id, f'<i>ваяяя</i> шеф, извиняй, опенаи не прикрутил костян пока', parse_mode='html')


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


# функция для пересылки сообщения из канала в чат
def forward_message(message):
    try:
        # получаем сообщение из канала
        channel_message = bot.forward_message(chat_id=112089205, from_chat_id=PLATFORM_TOILET_ID,
                                              message_id=message.message_id)
        # отправляем сообщение в чат
        bot.send_message(chat_id=112089205, text=channel_message.text)
    except Exception as e:
        logging.error(f"Ошибка при пересылке сообщения из канала в чат: {e}")


# обработчик новых сообщений в канале
@bot.channel_post_handler(func=lambda message: True)
def channel_post(message):
    # пересылаем сообщение в чат
    forward_message(message)


if __name__ == '__main__':
    logging.info("Бот запущен")
    bot.polling(none_stop=True)

schedule.every().day.at("18:00").do(leave_work_notification)


# функция для запуска check_in_genshin_notification() в отдельном потоке
def leave_work_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)


# запуск check_in_genshin_notification() в отдельном потоке
threading.Thread(target=leave_work_notification).start()

bot.polling(none_stop=True)
