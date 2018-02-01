import telebot
import os
import config
import requests
from flask import Flask, request

bot = telebot.TeleBot(config.token)

server = Flask(__name__)

bos.send_message(config.admin_id, 'I\'m online')

@bot.message_handler(commands=['start'])
def start(message):
    answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой :ООО"КомпозитСпецСтрой". Отправь мне /balance чтобы узнать о текущем состоянии счета.'%(message.from_user.first_name)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['balance'])
def balance(message):
	params = {'api_id':config.sms_token, 'json':1}
    result = requests.get('https://sms.ru/my/balance', params)
    if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
        balance = int(result.json().get('balance'))
        answer = 'Ваш баланс: ' + str(balance) + 'р.'
        else:
        	answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
    bot.send_message(message.chat.id, answer)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    answer = 'К сожалению, я не знаю эту команду. Но в будущем я собираюсь расширить свой функционал'
    bot.send_message(message.chat.id, answer)

@server.route("/"+config.token, methods=['GET', 'POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://kss-do-sms-bot.herokuapp.com/"+config.token)
    return "!", 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)

