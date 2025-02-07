import telebot
from flask import Flask, request
import os
from settings import API_TELEGRAM, WEBHOOK_URL # Импорт настроек

# Получаем токен бота из переменной окружения
BOT_TOKEN = API_TELEGRAM

# Создаем экземпляр бота
bot = telebot.TeleBot(BOT_TOKEN)

# WEBHOOK_URL = 'https://ваш_домен.ru/webhook' # URL вебхука теперь из settings.py или docker-compose.yml

# Создаем Flask приложение для обработки webhook
app = Flask(__name__)

application = app # Явно указываем WSGI application

# Установка вебхука при старте приложения (теперь не нужно явно удалять и устанавливать каждый раз)
# bot.remove_webhook() # Убираем, т.к. nginx проксирует запросы и не нужно дублировать
# bot.set_webhook(WEBHOOK_URL) # Убираем, т.к. вебхук устанавливается один раз через Telegram Bot API

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я простой бот.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)

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

# Flask App не запускается напрямую, это делает Gunicorn
# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 8443))
#     app.run(host='0.0.0.0', port=port)