from urllib import request
import time
import requests


def kurs(code):
    otvet = request.urlopen('https://www.cbr.ru/')
    mytext1 = str(otvet.read().decode(otvet.headers.get_content_charset()))
    t = mytext1.find(code)
    mytext1 = mytext1[t:]
    t = mytext1.find('</div>') - 7
    mytext1 = mytext1[t:t+7]
    return mytext1


def kursgrn():
    otvet = request.urlopen('https://www.banki.ru/products/currency/uah/')
    mytext1 = str(otvet.read().decode(otvet.headers.get_content_charset()))
    t = mytext1.find('<div class="currency-table__large-text">') + 40
    temp = list(mytext1[t:t + 5])
    t = temp.index(',')
    temp[t] = '.'
    return str(round((float("".join(temp)) / 10), 2))


def gismeteo(url):
    otvet = request.urlopen('https://www.gismeteo.ua/weather-donetsk-5080/')
    mytext1 = str(otvet.read().decode(otvet.headers.get_content_charset()))
    t = mytext1.find(url) + 37
    gismet = 'Gismeteo:\n'
    while mytext1[t] != '"':    # тут - состояние погоды, дождь снег и т.д.
        gismet += mytext1[t]
        t += 1
    mytext1 = mytext1[t:]
    t = mytext1.find('<span class="unit unit_temperature_c">') + 38  # запись от скольки градусов
    gismet += '\nТемпература от ' + mytext1[t: t+3] + ' до '
    mytext1 = mytext1[t:]
    t = mytext1.find('<span class="unit unit_temperature_c">') + 38  # до скольки
    gismet += mytext1[t: t+3]
    return gismet


def mailru(day):
    otvet = request.urlopen('https://pogoda.mail.ru/prognoz/donetsk/extended/')
    mytext1 = str(otvet.read().decode(otvet.headers.get_content_charset()))
    t = mytext1.find('<a name="' + day + '"></a>')
    mytext1 = mytext1[t:]
    sutki = ['Ночью', 'Утром', 'Днем', 'Вечером', ';']
    i = 0
    mail = ' Mail_ru:\n' + sutki[i] + '- '
    while i < 4:
        t = mytext1.find('<div class="day__date">' + sutki[i] + '</div>')
        mytext1 = mytext1[t:]
        t = mytext1.find('title="') + 7
        while mytext1[t] != '"':
            mail += mytext1[t]
            t += 1
        mytext1 = mytext1[t:]
        t = mytext1.find('<div class="day__temperature ">') + 31
        if i == 3:
            mail += ' ' + mytext1[t:t + 3] + ';'
        else:
            mail += ' ' + mytext1[t:t + 3] + ';\n' + sutki[i + 1] + ' - '
        i += 1
    return mail


def timeotime():
    dictionary = {'Mon': 'Понедельник', 'Tue': 'Вторник', 'Wed': 'Среда', 'Thu': 'Четверг',
                  'Fri': 'Пятница', 'Sat': 'Суббота', 'Sun': 'Воскресенье',
                  'Jan': 'Январь', 'Feb': 'Февраль', 'Mar': 'Март', 'Apr': 'Апрель',
                  'May': 'Май', 'Jun': 'Июнь', 'Jul': 'Июль', 'Aug': 'Август',
                  'Sep': 'Сентябрь', 'Oct': 'Октябрь', 'Nov': 'Ноябрь', 'Dec': 'Декабрь'}
    times = time.ctime(time.time())
    return "Сегодня:\nДень - " + dictionary.get(times[:3]) + ',\nМесяц - ' + dictionary.get(times[4:7]) +\
           ',\nЧисло - ' + times[8:10] + '-ое,\nВремя - ' + times[11:19] + ',\nГод - ' + times[19:] + ';'


def inet():
    otvet = request.urlopen('http://room.telephant.org/area/handler.php?'
                            'login_name=b4096k401611&login_password=7623191233')
    mytext1 = str(otvet.read().decode(otvet.headers.get_content_charset()))
    restext = ' Лицевой счёт - '
    t = mytext1.find('Лицевой счет') + 20
    mytext1 = mytext1[t:]
    t = mytext1.find('>') + 1
    mytext1 = mytext1[t:]
    t = mytext1.find('<')
    restext += mytext1[:t] + ';\nБаланс - '
    t = mytext1.find('Текущий баланс') + 20
    mytext1 = mytext1[t:]
    t = mytext1.find('>') + 1
    mytext1 = mytext1[t:]
    t = mytext1.find('<')
    mytext1 = mytext1[:t]
    restext += mytext1 + ';'
    return restext


def oniksmoney():
    s = requests.Session()
    data = {
        'j_username': '+380713671228',
        'j_password': 'Green-haired_roses',
    }
    s.post('https://oniks.money/clients/loginProcess', data=data)
    r = (s.get('https://oniks.money')).text
    t = r.find('<span class="title">RUB ') + 24
    r = 'На счету OniksMoney : ' + r[t:t+6] + ' рублей'
    return r


def checkgaz():
    s = requests.Session()
    data = {
        'identity': 'kurkurin2001@yandex.com',
        'password': 'Nek0507677684',
        'csrf_token': 'cfae45a5db789886f729d16fff9e63ea',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    }
    s.post('https://www.komservice.center/user/login/', data=data, headers=headers)
    r = (s.get('https://www.komservice.center/carddata/card_data/84243', headers=headers)).text
    t = r.find('Задол')
    if t == -1:
        t = r.find('Переп')
    r = r[t:]
    t = r.find('<')
    _r = r[:t] + ' '
    t = r.find('>') + 1
    _r += r[t:t+6]
    result = 'Ваш счет за ГАЗ : ' + _r + ' рублей;\n'
    t = r.find('Последние показания:')
    r = r[t:]
    t = r.find('от') + 3
    r = r[t:t+11]
    result += 'Дата последних обновлений: ' + r + ';'
    return result


def kino(title):
    preurl = 'https://kinoframe.net/search/' + title + '/'
    s = requests.Session()
    r = s.get(preurl).text
    dict_of_films_unsorted = {}  # ссылки + названия фильмов
    while True:
        t = r.find('<div class="thumbnail">')
        if t == -1:
            break
        r = r[t:]
        t = r.find('title="Фильм ') + 13
        title = r[t: r.find(' скачать')]
        t = r.find('<a href="') + 9
        r = r[t:]
        url = 'https://kinoframe.net' + r[:r.find('"')]
        r = r[t:]
        dict_of_films_unsorted.update({title: url})
    dict_of_films = {}
    for i in sorted(dict_of_films_unsorted):
        dict_of_films.update({i: dict_of_films_unsorted[i]})
    return dict_of_films


def choice_quality(url_of_film):
    s = requests.Session()
    r = s.get(url_of_film).text
    dict_of_quality = {}
    while True:
        t = r.find('<tr><td>')
        if t == -1:
            break
        r = r[t:]
        t = r.find('href="') + 6
        url = 'https://kinoframe.net' + r[t: r.find('title') - 2]
        t = r.find('title="Скачать торрент" style="font-weight: bold;">') + 51
        quality = r[t: r.find('</a>')]
        r = r[r.find('</a>'):]
        dict_of_quality.update({quality: url})
    return dict_of_quality


def game(title):
    s = requests.Session()
    data = {'do': 'search',
            'subaction': 'search',
            'search_start': '1',  # для некст стр + 1
            'full_search': '0',
            'result_from': '1',  # для некст стр + 15
            'story': title,
            }

    r = s.post('http://gmt-max.net/index.php?do=search', data=data).text
    dict_of_games = {}
    while r.find('<div class="short_news_title_center">') != -1:
        r = r[r.find('<div class="short_news_title_center">') + 46:]
        url = r[: r.find('"')]
        title = r[r.find('>') + 1: r.find('<')]
        r = r[r.find('</div>'):]
        dict_of_games.update({title: url})
    return dict_of_games


def download_game(game):
    s = requests.Session()
    r = s.get(game).text
    r = r[r.find('<div class="title">') + 19:]
    return 'http://gmt-max.net' + r[r.find('"') + 1: r.find('>') - 1]

