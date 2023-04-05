import datetime
import random


def where_are_yura():
    now = datetime.datetime.now()  # получаем текущее время
    sleep_time = datetime.time(8, 30, 0)
    taxi_morning_time = datetime.time(10, 5, 0)
    working_time = datetime.time(19, 30, 0)
    taxi_evening_time = datetime.time(21, 0, 0)
    if now.time() <= sleep_time:
        return 'шеф, я сейчас сплю =) напиши попозже всё порешаем все вопросики'
    elif now.time() <= taxi_morning_time:
        return 'началник, МАКСИМАЛНО еду на такси, на дейлик опоздаю на 5 минут, не бей тока'
    elif now.time() <= working_time:
        chance = random.randint(1, 100)
        if chance >= 20:
            return 'ЧЕГО ТЫ ОПЯТЬ СИДИШЬ РАБОТАЕШЬ, курить пойдем =)'
        else:
            return 'балин я работаю МОЩНО, ничего не успеваю =('
    elif now.time() <= taxi_evening_time:
        return 'бро, я уже домой еду, давай завтра поправлю все баги и выкачу'
    else:
        return 'ваяяя я тут МОЩНО сижу дома кайфую =)'
