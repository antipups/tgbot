import requests
import telebot
import sys
from urllib import request
import pprint
import datetime
import time
import show
import os
from telebot import types
from pyaspeller import YandexSpeller


TOKEN = '914271777:AAEJol6pCnAyLRQbAEeRz0cOPzZtgeDrero'
bot = telebot.TeleBot(TOKEN)
adminid = 704369002
lshelp = ['help',
          'command',
          'помощь',
          'команды',
          ]
lsabout = ['about',
           'о',
           'о разработчике',
           ]


@bot.message_handler(commands=lshelp)
def kek(message):
    text = """ Доступные команды :>
    /about - о разработчике;
    время - показывает время;
    курс евро / доллара / гривны - показывает курс евро / доллара / гривны  к рублю;
    где я - показывает ваше местоположение на карте;
    погода завтра / сегодня - погода на завтра / сегодня в Донецке;
    деньги - счета на вебкошелях;
    проверка текста - исправление ошибок в введенном тексте;
    скачать фильм / - скачать фильм /"""

    if message.from_user.id == adminid:
        text += """
        интернет - лиц. счет и тек. баланс;
        газ - проверка счета газа"""

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=lsabout)
def url(message):
    bot.send_photo(message.chat.id, 'https://pp.userapi.com/c846219/v846219134/cba35/puXnXwYcw7Y.jpg')
    markup = types.InlineKeyboardMarkup()
    btn_my_site = types.InlineKeyboardButton(text='ВК', url='https://vk.com/antipupsik')
    markup.add(btn_my_site)
    btn_my_site = types.InlineKeyboardButton(text='Телега', url='https://t.me/OnionBerserker')
    markup.add(btn_my_site)
    bot.send_message(message.chat.id, ' ФИО - Куркурин Никита Леонидович;'
                                      '\nКонтактные данные - \n', reply_markup=markup)


#   МЕСТОПОЛОЖЕНИЕ
def buttonloc():    # фиксированная кнопка, появляющаяся внизу экрана
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton(text="Узнать свое местоположение",  request_location=True)
    markup.add(btn1)
    return markup


#   ПРОВЕРКА ТЕКСТА
def checkgraf(message):
    msg = bot.send_message(message.chat.id, 'Введите текст :> ')
    bot.register_next_step_handler(msg, corrgraf)


def corrgraf(message):
    _text = message.text
    speller = YandexSpeller()
    try:
        changes = {change['word']: change['s'][0] for change in speller.spell(_text)}
        for word, suggestion in changes.items():
            _text = _text.replace(word, suggestion)
    except IndexError:
        bot.send_message(message.from_user.id, 'Определенного слова нет в словаре')
    else:
        bot.send_message(message.from_user.id, 'Проверенный текст :> \n' + _text)


# ДЛЯ ФИЛЬМОВ
def checkfilm(message):
    msg = bot.send_message(message.chat.id, 'Введите название фильма :> ')
    bot.register_next_step_handler(msg, mainfilm)


def mainfilm(message):
    markup = types.InlineKeyboardMarkup()
    _text = message.text
    print(_text)
    dict_ = show.downloadfilm(_text)
    if len(dict_) < 1:
        bot.send_message(message.from_user.id, 'Введенного фильма не было найдено на сайте,\n'
                                               'проверьте название фильма, оно должно быть:\n'
                                               '- начинатся с большой буквы;\n'
                                               '- желательно оригинальное название(на англ);\n')
    else:
        for ls in dict_.items():
            tempurl = str(ls[0])
            if sys.getsizeof(tempurl) > 100:
                tempurl = tempurl[:50]
            markup.add(types.InlineKeyboardButton(text=ls[1], callback_data=tempurl))
        bot.send_message(message.from_user.id, 'Выберете в каком качестве качать :> ', reply_markup=markup)


# КНОПКА ДОТЫ
def buttondota():
    markup = types.InlineKeyboardMarkup()
    dict_ = show.dotaupdates()
    for ls in dict_.items():
        tempurl = str(ls[1])
        if sys.getsizeof(tempurl) > 100:
            tempurl = tempurl[:50]
        markup.add(types.InlineKeyboardButton(text=ls[0], callback_data=tempurl))
    return markup


@bot.callback_query_handler(func=lambda message: True)
def dotanews(url1):
    if url1.data.find('/torrents/') != -1:  # скачивание фильмов
        namefile = 'Нажми.torrent'
        request.urlretrieve('https://kinoframe.net' + url1.data, namefile)
        with open(namefile, 'rb') as f:
            os.startfile(namefile)
            time.sleep(60)
        # os.remove(namefile)
    # elif url1.data.find('/news/') != -1:    # дота новости
    #     result = show.dotanews(url1.data)
    #     bot.send_message(url1.from_user.id, result)


@bot.message_handler(content_types=["text"])
def test(message):
    text = message.text
    userid = message.from_user.id
    if text.find('курс') != -1:
        if text.find('доллара') != -1:
            bot.send_message(userid, '$$$ Курс доллара к рублю - 1 : ' + show.kurs('Доллар'))
        elif text.find('евро') != -1:
            bot.send_message(userid, '€€€ Курс евро к рублю - 1 : ' + show.kurs('Евро'))
        elif text.find('гривны') != -1:
            bot.send_message(userid, '₴₴₴ Курс гривны к рублю - 1 : ' + show.kursgrn())
    if text.find('погода') != -1:
        if text.find('сегодня') != -1:
            bot.send_message(userid, show.gismeteo('<div class="tab  tooltip" data-text="'))
            bot.send_message(userid, show.mailru('day1'))
        if text.find('завтра') != -1:
            bot.send_message(userid, show.gismeteo('r-donetsk-5080/tomorrow/" data-text="'))
            bot.send_message(userid,  show.mailru('day2'))
    elif text.find('время') != -1:
        bot.send_message(userid, show.timeotime())
    elif text.find('где я') != -1:
        bot.send_message(userid, 'Ваши координаты :> ', reply_markup=buttonloc())
    elif text.find('интернет') != -1:
        if userid == adminid:
            bot.send_message(userid, show.inet())
    elif text.find('деньги') != -1:
        bot.send_message(userid, show.oniksmoney())
    elif text.find('газ') != -1:
        if userid == adminid:
            bot.send_message(userid, show.checkgaz())
    elif text.find('проверка текста') != -1:
        checkgraf(message)  # нельзя в другом файле, так как отправка сообщения только через сенд месс, иначе краш
    elif text.find('дота') != -1:
        bot.send_message(userid, 'Новости Доты :', reply_markup=buttondota())
    elif text.find('скачать') != -1:
        if text.find('фильм') != -1:
            checkfilm(message)


print("I'm Work!")
bot.infinity_polling(True)
