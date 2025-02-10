import telebot
from flask import Flask, request
import os
from settings import API_TELEGRAM, WEBHOOK_URL # Импорт настроек

# Получаем токен бота из переменной окружения
BOT_TOKEN = API_TELEGRAM

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# Создаем Flask приложение для обработки webhook
app = Flask(__name__)

application = app # Явно указываем WSGI application

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я простой бот.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello World from Flask App!"

# Обработчик webhook (путь должен совпадать с тем, что в Nginx и Dockerfile)
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200 # Важно вернуть 'OK' для Telegram
    else:
        return 'invalid request', 403