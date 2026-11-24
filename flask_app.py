# A very simple Flask Hello World app for you to get started with...
import random
from flask import Flask, request

app = Flask(__name__)

@app.route('/lati')
def lati_command():
    user = request.args.get('user', 'Аноним')
    nick = user.lower().strip()

    # Жесткая проверка: если это не Лати, возвращаем сообщение
    if nick != 'laatteeeee_':
        return "Ты не Лати -_-"

    # Базовые переменные
    real_name = "Лати"
    fake_name = "Светочка"

    # Свапаем имена с шансом 50/50
    if random.random() < 0.5:
        real_name, fake_name = fake_name, real_name

    # Формируем ответ через f-строку
    return f"Привет, {real_name}! Мы помним, что ты не {fake_name}"
