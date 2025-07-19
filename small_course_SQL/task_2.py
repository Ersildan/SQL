import sqlite3

"""Задание обменник валюты"""


"""Создаем базу данных users_balance"""

db = sqlite3.connect('exchanger.db') # Создаем и подключаем БД
cur = db.cursor() # Переменная для управления БД
print("1. Создали и подключились к базе данных exchanger.db")


"""Создаём таблицу users_data, если она не создана.
Задаем названия и тип данных для колонок."""
cur.execute("""
    CREATE TABLE IF NOT EXISTS users_balance(
    UserID TEXT PRIMARY KEY,
    Balance_RUB FLOAT NOT NULL,
    Balance_USD FLOAT NOT NULL,
    Balance_EUR FLOAT NOT NULL
    );""")
print("2. Создали таблицу users_balance и задали типы данных для колонок")


"""Вносим первого пользователя в таблицу.
Безопасным способом от SQL-инъекций.
Игнорируем вставку, если он уже есть."""

money_params = ('Брюс Уэйн', 1000000.0, 1000.0, 100.0)
cur.execute("""
    INSERT OR IGNORE INTO users_balance (UserID, Balance_RUB, Balance_USD, Balance_EUR)
        VALUES (?, ?, ?, ?)""", money_params)
db.commit() # Сохраняем все изменения
print()

# txt = """Добро пожаловать в Бэт-обменник 💰
# Какую валюту хотите получить?
# Введите [ 1 ] если меняем (USD или EUR) на рубли
# Введите [ 2 ] если меняем (RUB или EUR) на баксы
# Введите [ 3 ] если меняем (RUB или USD) на евро
# """
# print(txt)

txt2 = """Курс валют:
1 USD = 70 RUB
1 EUR = 80 RUB
1 USD = 0,87 EUR
1 EUR = 1,15 USD"""

def check_summa(summa, choice):
    """Проверяем правильность ввода и хватит ли денег для обмена валюты"""

    if summa.isdigit() is not True:
        raise Exception ('Ошибка: Нужно ввести цифры без букв')

    cur.execute("""SELECT * FROM users_balance;""") # Читаем баланс в таблицу users_balance

    balance = cur.fetchone()
    balance_usd = balance[int(choice) + 1]

    if int(summa) > balance_usd:
        raise Exception ('\033[31mНедостаточно средств USD для обмена на RUB.\033[0m\n'
                        f'На балансе доступно: {balance_usd} $\n'
                         'Повторите попытку')

    else:
        print(f'Совершен обмен валют {summa}$. '
              f'На балансе USD: {balance_usd - int(summa)}$\n'
              f'Пополнение счета RUB на {int(summa) * 70}р. Баланс RUB: {balance[int(choice)] + int(summa) * 70}р')

def func_rub():
    """Меняем (USD или EUR) на рубли"""
    while True:
        try:
            txt = "Введите [ 1 ] если отдаёте USD\nВведите [ 2 ] если отдаёте EUR\nЧтобы выйти введите любой символ"
            print(txt)

            choice = input()

            if choice == '1':
                print('Сколько хотите отдать USD?')
            elif choice == '2':
                print('Сколько хотите отдать EUR')
            else:
                exit('Выход из обменника')

            summa = input()

            check_summa(summa, choice) # Вызываем функцию для проверки остатка и правильность ввода числа
            break
        except Exception as e:
            print(e)

func_rub()


# match input().lower():
#     case 1, 'rub':
#         print()
#     case 2, 'usd':
#         print()
#     case 3, 'eur':
#         print()