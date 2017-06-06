import requests
from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
import sqlite3

# Для отправки СМС уведомления!
import urllib
import urllib.request
import json
from datetime import datetime, date, time

def send_sms(phones, text, total_price=0):
    login = 'skridlkats'  # Логин в smsc
    password = 'ugufig95'  # Пароль в smsc
    sender = 'py_test'  # Имя отправителя
    # Возможные ошибки
    errors = {
        1: 'Ошибка в параметрах.',
        2: 'Неверный логин или пароль.',
        3: 'Недостаточно средств на счете Клиента.',
        4: 'IP-адрес временно заблокирован из-за частых ошибок в запросах. Подробнее',
        5: 'Неверный формат даты.',
        6: 'Сообщение запрещено (по тексту или по имени отправителя).',
        7: 'Неверный формат номера телефона.',
        8: 'Сообщение на указанный номер не может быть доставлено.',
        9: 'Отправка более одного одинакового запроса на передачу SMS-сообщения либо более пяти одинаковых запросов на получение стоимости сообщения в течение минуты. '
    }
    # Отправка запроса
    url = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s&cost=%d&sender=%s&fmt=3" % (
    login, password, phones, text, total_price, sender)
    answer = json.loads(urllib.request.urlopen(url).read())
    if 'error_code' in answer:
        # Возникла ошибка
        return errors[answer['error_code']]
    else:
        if total_price == 1:
            # Не отправлять, узнать только цену
            print('Будут отправлены: %d SMS, цена рассылки: %s' % (answer['cnt'], answer['cost'].encode('utf-8')))
        else:
            # СМС отправлен, ответ сервера
            return answer

# Приветствие  зависимости от времени
data = datetime.strftime(datetime.now(), "%d.%m.%Y")
time = datetime.strftime(datetime.now(), "%H:%M:%S")

if datetime.strftime(datetime.now(), "%H") <= '12' and datetime.strftime(datetime.now(), "%H") >= '5':
    a = 'Good morning,'
elif datetime.strftime(datetime.now(), "%H") >= '12' and datetime.strftime(datetime.now(), "%H") <= '17':
    a = 'Good afternoon,'
else:
    a = 'Good evening,'

con = sqlite3.connect('db.sqlite3')
cur = con.cursor()
cur.execute('SELECT * FROM blog_post')

for row in cur:
    sms = []  # Создание текста сообщения
    nam_id = row[1]  # Имя пользователя
    sms.append(a)
    sms.append(nam_id)
    if row[3] == 1: # Погода
        url1 = 'https://weather.rambler.ru/v-sankt-peterburge/'  # Wearher
        response = requests.get(url1)
        page1 = BeautifulSoup(response.text, 'html.parser')
        tem = page1.findAll(attrs={"href": "/v-sankt-peterburge/7-june/"})[2].string[21::20]
        sms.append('Temperature: {tem}*'.format(tem=tem))
    else:
        pass
    if row[9] == 1: # Пробки
        url2 = 'http://www.roads.gorodovoy.spb.ru/'  # Probki
        response = requests.get(url2)
        page2 = BeautifulSoup(response.text, 'html.parser')
        # prob = page2.findAll(attrs={"class": "YMaps-traffic-button-content__traffic-level"})
        prob = 2
        sms.append('Situation on the road :{prob}'.format(prob=prob))
    else:
        pass
    if row[8] == 1: # Курс валют
        url = 'http://www.banki.ru/products/currency/cash/sankt-peterburg/'
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        usd = page.findAll('div', {'class': 'currency-table__large-text'})[0].string
        eur = page.findAll('div', {'class': 'currency-table__large-text'})[3].string
        sms.append('USD: {usd}, EUR: {eur}'.format(usd=usd, eur=eur))
    else:
        pass
    if row[7] != '':  # Задача/напоминаиние
        sms.append('Task: {n}'.format(n=row[7]))  # Tasks
    else:
        pass

    sms_id = ' '.join(sms) # провожу сообщение в строку
    num_id = row[2]  # Номер пользователя
    tim_id = row[5][:-3] # Время в формате час:мин

    if tim_id == datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"): # проверка времени отправки сообщения с местным времением
        print(send_sms(num_id, sms_id))  # отвечает за отправку сообщения
        send=['Сообщение успешно отправлено', nam_id]
    else:
        send=['Сообщение не отправлено!', nam_id, sms_id]
    print(send)
con.close()


# def run():
#     with daemon.DaemonContext():
#         sms_letter()
#
# if __name__ == '__main__':
#     run(none_stop=True)