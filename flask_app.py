# A very simple Flask Hello World app for you to get started with...
import random
from flask import Flask, request

app = Flask(__name__)

@app.route('/whoami')
def whoami():
    # 1. Получаем параметр ?user= от Nightbot (если его нет, пишем 'Аноним')
    user = request.args.get('user', 'Аноним')
    nick = user.lower().strip()

    # 2. Словарь (база данных) особых пользователей чата
    special_users = {
        'malinus_keshar': 'Шиз',
        'mod_alex': 'Шериф чата',
        'vip_user77': 'Главный спонсор'
    }

    display_name = user

    # 3. Сложная логика с рандомом для laatteeeee_ (30% шанс на СекретноеИмя)
    if nick == 'laatteeeee_':
        display_name = 'Светочка' if random.random() < 0.3 else 'Лати'

    # 4. Если это не Лати, проверяем по общему списку замен
    elif nick in special_users:
        display_name = special_users[nick]

    # 5. Формируем красивый ответ в стиле ИИ
    # response_text = f"Сканирование сетчатки... Личность подтверждена. Добро пожаловать, {display_name}."
    response_text = "Ты {}.".format(display_name)

    # Возвращаем чистый текст для Nightbot
    return response_text

@app.route('/lati')
def lati_command():
    user = request.args.get('user', 'Аноним')
    nick = user.lower().strip()

    # Жесткая проверка: если это не Лати, возвращаем пустоту
    if nick != 'laatteeeee_':
        return ""

    # Базовые переменные
    real_name = "Лати"
    fake_name = "Светочка"

    # Свапаем имена с шансом 50/50
    if random.random() < 0.5:
        real_name, fake_name = fake_name, real_name

    # Формируем ответ через f-строку
    return f"Привет, {real_name}! Мы помним, что ты не {fake_name}"
