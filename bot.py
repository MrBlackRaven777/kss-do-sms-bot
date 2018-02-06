import telebot
import os
import config
import requests
import utils
from config import u_states as states
from flask import Flask, request

bot = telebot.TeleBot(config.token)

server = Flask(__name__)

numbers_string = ''
#bot.send_message(config.admin_id, 'I\'m online')

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

@bot.message_handler(commands=['cost'])
def cost_start(message):
    chat_id = message.chat.id
    utils.shelve_write(id=chat_id, state=states.U_ASK_COST)
    answer = 'Введите список номеров для проверки стоимости. Все номера должны быть в одном сообщении, в теле номера не должно быть пробелов.'
    bot.send_message(chat_id, answer)

@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ASK_COST)
def cost_phones(message):
    global numbers_string
    chat_id = message.chat.id
    try:
        numbers_list = utils.format_numbers(message.text, '0')
        postfix = 'а' if len(numbers_list)>1 else ''
        answer = 'Вы прислали мне номер' + postfix + ': ' + '\n'.join(numbers_list) + '.\nЕсли что-то введено неправильно, нажмите /cost и введите номера заново. Введите текст сообщения:'
        utils.shelve_write(chat_id, states.U_ENT_PHONES)
        numbers_string = ','.join(utils.format_numbers(message.text, '2'))
    except TypeError:
        answer = 'Проверьте правильность введенных номеров'
    bot.send_message(chat_id, answer)
    

#@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ENT_PHONES)
#def cost_total(message):
#    global numbers_string
#    numbers = utils.format_numbers(message.message_id(message.message_id-1).text)
#
#    params = {'api_id':config.sms_token, 'to' : numbers_string, 'msg' : message.text, 'json':1}
#    try:
#        result = requests.get('https://sms.ru/my/cost', params)
#        if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
#            cost = int(result.json().get('total_cost'))
#            sms_count = result.json().get('total_sms')
#            answer = 'Стоимость отправки <b>%d</b> sms составит <b>%d</b>р.'%(sms_count, cost)
#        else:
#            answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
#    except TypeError:
#        answer = 'Проверьте правильность введенных номеров'
#    bot.send_message(chat_id, answer, parse_mode='markdown')


@bot.message_handler(commands=['test'])
def test(message):
    prev_msg = message.message_id(message.message_id-1).text
    prevprev_msg = message.message_id(message.message_id-2).text
    answer = 'Previous message id:\n<b>%s</b>\nPrevious message text:\n<b>%s</b>\nPrePrevious message id:\n<b>%s</b>\nPrePrevious message text:\n<b>%s</b>\n'%(message.message_id-1, prev_msg,message.message_id-2,prevprev_msg)
    chat_id = message.chat.id
    bot.send_message(chat_id, answer, parse_mode='markdown')


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

