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

# Приветствие
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
    sms = []  # Создание текста сообщения ''
    n = row[1]  # Имя пользователя

    if row[3] == 1 and row[4] == 1 and row[7] != '':
        url1 = 'https://weather.rambler.ru/v-sankt-peterburge/'   #Wearher
        response = requests.get(url1)
        page1 = BeautifulSoup(response.text, 'html.parser')
        tem = page1.findAll(attrs={"href": "/v-sankt-peterburge/5-june/"})[2].string[21::20]
        t ='Temperature: {tem}*'.format(tem=tem)

        url2 = 'http://www.roads.gorodovoy.spb.ru/'   # Probki
        response = requests.get(url2)
        page2 = BeautifulSoup(response.text, 'html.parser')
                    # prob = page2.findAll(attrs={"class": "YMaps-traffic-button-content__traffic-level"})
        prob = 2
        p = 'Situation on the road :{prob}'.format(prob=prob)

        s = 'Task: {n}'.format(n=row[7])   #Tasks
        sms.append('{a}{n}! {s}! {t}, {p}'.format(a=a, n=n, s=s, t=t, p=p))

    elif row[3] == 0 and row[4] == 1 and row[7] != '':
        url2 = 'http://www.roads.gorodovoy.spb.ru/'  # Probki
        response = requests.get(url2)
        page2 = BeautifulSoup(response.text, 'html.parser')
                    # prob = page2.findAll(attrs={"class": "YMaps-traffic-button-content__traffic-level"})
        prob = 2
        p = 'Situation on the road :{prob}'.format(prob=prob)

        s = 'Task: {n}'.format(n=row[7])  # Tasks
        sms.append('{a}{n}! {s}! {p}'.format(a=a, n=n, s=s, p=p))

    elif row[3] == 1 and row[4] == 0 and row[7] != '':
        url1 = 'https://weather.rambler.ru/v-sankt-peterburge/'  # Wearher
        response = requests.get(url1)
        page1 = BeautifulSoup(response.text, 'html.parser')
        tem = page1.findAll(attrs={"href": "/v-sankt-peterburge/5-june/"})[2].string[21::20]
        t = 'Temperature: {tem}*'.format(tem=tem)

        s = 'Task: {n}'.format(n=row[7])  # Tasks
        sms.append('{a}{n}! {s}! {t}'.format(a=a, n=n, s=s, t=t))

    elif row[3] == 1 and row[4] == 1 and row[7] == '':
        url1 = 'https://weather.rambler.ru/v-sankt-peterburge/'  # Wearher
        response = requests.get(url1)
        page1 = BeautifulSoup(response.text, 'html.parser')
        tem = page1.findAll(attrs={"href": "/v-sankt-peterburge/5-june/"})[2].string[21::20]
        t = 'Temperature: {tem}*'.format(tem=tem)

        url2 = 'http://www.roads.gorodovoy.spb.ru/'  # Probki
        response = requests.get(url2)
        page2 = BeautifulSoup(response.text, 'html.parser')
                    # prob = page2.findAll(attrs={"class": "YMaps-traffic-button-content__traffic-level"})
        prob = 2
        p = 'Situation on the road :{prob}'.format(prob=prob)

        sms.append('{a}{n}! {t}, {p}'.format(a=a, n=n, p=p, t=t))

    elif row[3] == 0 and row[4] == 0 and row[7] != '':

        s = 'Task: {n}'.format(n=row[7])  # Tasks
        sms.append('{a}{n}! {s}!'.format(a=a, n=n, s=s))

    elif row[3] == 1 and row[4] == 0 and row[7] == '':
        url1 = 'https://weather.rambler.ru/v-sankt-peterburge/'  # Wearher
        response = requests.get(url1)
        page1 = BeautifulSoup(response.text, 'html.parser')
        tem = page1.findAll(attrs={"href": "/v-sankt-peterburge/5-june/"})[2].string[21::20]
        t = 'Temperature: {tem}*'.format(tem=tem)

        sms.append('{a}{n}! {t}'.format(a=a, n=n, t=t))
    else:
        sms.append('{a}{n}!'.format(a=a, n=n))
    sms_id = ''.join(sms)
    num_id = row[2]  # Номер пользователя
    tim_id = row[8][:-3]
    nam_id = row[1]

    if tim_id == datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M"):
        print(send_sms(num_id, sms_id))
        prin=['Сообщение успешно отправлено', nam_id]
    else:
        prin=['Сообщение не отправлено!', nam_id]
    print(prin)
con.close()


# def run():
#     with daemon.DaemonContext():
#         sms_letter()
#
# if __name__ == '__main__':
#     run(none_stop=True)