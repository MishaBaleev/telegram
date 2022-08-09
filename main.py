# ********************
# телеграмм-бот, написанный при помощи библиотеки Python3 telebot
# имя бота в телеграмме - @O_S_I_N_T_Bbon_bot
# ********************

import telebot
from telebot import types 
import socket
import requests
import datetime

# function функция получения ip адреса по доменному имени
def get_ip_by_domain(website):
    try: 
        return f'Имя: {website}\nIP-адрес: {socket.gethostbyname(website)}'
    except: 
        return 'Проверьте написание доменного имени.'
# funtion

# function функция получения информации по ip адресу 
def get_info_by_ip(ip):
    response = requests.get(url=f'http://ip-api.com/json/{ip}').json()

    data = {
        'IP': response.get('query'),
        'Провайдер': response.get('isp'),
        'Организация': response.get('org'),
        'Страна': response.get('country'),
        'Регион': response.get('regionName'),
        'Город': response.get('city'),
        'Индекс': response.get('zip'),
        'Долгота': response.get('lat'),
        'Широта': response.get('lon'),
    }

    result = ''
    for k, v in data.items():
        result = result + str(k) + ' : ' + str(v) + '\n'

    return result
# function

# function функция получения погодной информации по населенному пункту и токену
# токен известен заранее
def get_info_weather (place, weather_token):
    try: 
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

        return (f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                f"Погода в городе: {city}\nТемпература: {cur_weather} C°\n"
                f"Влажность: {humidity} %\nСкорость ветра: {wind} м/с\n"
                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                )
    except: 
        return 'Проверьте написание города.'
# function

# function функция для правильного разделения строки исходного сообщения 
def parcing_str (line):
    if line.find(': ') > -1:
        return True
    else:
        return False
# function

#bot тело бота, в котором описана логика бота
token = '5415603385:AAFL-lZuhKvf0z18xoRRusV3tqS0lKU9nGQ' # токен телеграмм-бота
bot = telebot.TeleBot (token)

# действия бота при команде start
@bot.message_handler  (commands=['start']) 
def start(message):
    reply = types.ReplyKeyboardMarkup (resize_keyboard = True)
    manual = types.KeyboardButton ('ИНСТРУКЦИЯ')
    callBack = types.KeyboardButton ('ОБРАТНАЯ СВЯЗЬ')
    reply.add (manual, callBack)
    bot.send_message(message.chat.id, 'привет привет', reply_markup = reply)

# действия бота при текстовом сообщении
@bot.message_handler (content_types = ['text']) 
def send_text(message):

    if message.text == 'ИНСТРУКЦИЯ':
        bot.send_message (message.chat.id, 'Узнать погоду\nПример | погода: Москва\n**********\nУзнать IP\nПример | ip: 8.8.8.8\n**********\nУзнать IP по доменному имени\nПример | домен: google.com')
    elif message.text == 'ОБРАТНАЯ СВЯЗЬ':
        callbackRef = types.InlineKeyboardMarkup ()
        developer = types.InlineKeyboardButton ('Напиши мне', url = 'https://t.me/Bbon2476')
        callbackRef.add (developer)
        bot.send_message (message.chat.id, 'Если появились вопросы или теплые слова.', reply_markup = callbackRef)
    else: 
         # блок проверки на тип команды, с пробелом или без
        if parcing_str(message.text) == True:
            messageText = message.text.lower()
            command = messageText.split(': ')[0]
            split = ': '
        elif parcing_str(message.text) == False:
            messageText = message.text.lower()
            command = messageText.split(':')[0]
            split = ':'

        # блок ответов на пользовательские сообщения 
        if command == 'domain' or command == 'домен':
            text = get_ip_by_domain(messageText.split(split)[1])
            bot.send_message (message.chat.id, text)
        elif command == 'ip' or command == 'айпи':
            markup = types.InlineKeyboardMarkup ()
            map = types.InlineKeyboardButton ('Открыть карту', url = 'https://yandex.ru/maps/geo/rossiya/53000001/?ll=105.306388%2C69.674041&z=2.97')
            markup.add (map)
            text = get_info_by_ip(messageText.split(split)[1])
            bot.send_message (message.chat.id, text, reply_markup = markup)
        elif command == 'weather' or command == 'погода':
            weather_token = 'c1e431a75aaa295d32b36fb1d96538fd'
            text = get_info_weather(messageText.split(split)[1], weather_token)
            bot.send_message (message.chat.id, text)
        else:
            text = 'К сожалению, неправильная команда, попробуйте переосмыслить инструкцию.'
            bot.send_message (message.chat.id, text)

bot.polling(non_stop=True) # для того, чтобы бот мониторил сообщения адекватно

    
