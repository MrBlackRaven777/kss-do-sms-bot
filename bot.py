import telebot
import os
import config
import requests
import utils
import sys
from config import u_states as states
from flask import Flask, request

bot = telebot.TeleBot(config.token)

server = Flask(__name__)

numbers_string = ''
sending_message = ''
#bot.send_message(config.admin_id, 'I\'m online')

def check_id(id):
    print('check_id is on action')
    if config.public_mode_on == False:
        if str(id) in config.admin_ids:
            return True
        else:
            bot.send_message(id, 'Отказано в доступе')
            if config.notify_admins == True:
                user = bot.get_chat(id)
                user_info = 'В бот стучится неавторизованный пользователь: <b>%s %s</b>;\nUsername: <b>@%s</b>;\nid: <b>%s</b>.'%(user.first_name, user.last_name, user.username, user.id)
                for adm_id in config.admin_ids:
                    bot.send_message(int(adm_id), user_info, parse_mode='HTML')
            return False

def notifier(delay):
    with shelve.open('nodes') as nodes_storage:
        nodes_dict = dict(nodes_storage)
        
    discharged = account.inbox / 'MeshLogic' / 'Разряжаются'
    if discharged.unread_count > 0:
        pattern = re.compile('([_\d]{7,9}).*([,\d]{5}).*(\d{2}\.\d{2}\.\d{4}).*(\d{2}\:\d{2}\:\d{2}).*([0-9,]{5}).*(\d{2}\.\d{2}\.\d{4}).*(\d{2}\:\d{2}\:\d{2})', re.DOTALL)
        for item in discharged.filter(is_read=False):
#            print(item.body)
            r = re.findall(pattern, item.body)
            print(r)
            print(r[0][0])
            node = str(r[0][0])[:str(r[0][0]).find('_')]
            print(node)
            msg = 'Оповещение Нахимовский:\n%s в %s узел %s (У%s) разрядился до %sВ'%(r[0][2], r[0][3], node, nodes_dict.get(node), r[0][1])
            print(msg)
            print(item.is_read)
            item.is_read = True
            item.save
    del nodes_dict
    time.sleep(delay)
    notifier(delay)

@bot.message_handler(commands=['start'], func=lambda message: check_id(message.chat.id))
def start(message):
    answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой ООО"КомпозитСпецСтрой". Отправь мне /help чтобы узнать о всех моих функциях.'%(message.from_user.first_name)
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['balance'], func=lambda message: check_id(message.chat.id))
def balance(message):
    params = {'api_id':config.sms_token, 'json':1}
    result = requests.get('https://sms.ru/my/balance', params)
    if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
        balance = round(result.json().get('balance'), 2)
        answer = 'Ваш баланс: <b>%s р.</b>'%(balance)
    else:
        answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
    bot.send_message(message.chat.id, answer, parse_mode='HTML')

@bot.message_handler(commands=['cost'], func=lambda message: check_id(message.chat.id))
def cost_start(message):
    chat_id = message.chat.id
    utils.shelve_write(id=chat_id, state=states.U_ASK_COST)
    answer = 'Введите список номеров для проверки стоимости. Все номера должны быть в одном сообщении, в теле номера не должно быть пробелов.'
    bot.send_message(chat_id, answer)

@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ASK_COST and check_id(message.chat.id), content_types=['text'])
def cost_phones(message):
    global numbers_string
    chat_id = message.chat.id
    try:
        numbers_list = utils.format_numbers(message.text, '0')
        postfix = 'а' if len(numbers_list)>1 else ''
        answer = 'Вы прислали мне номер' + postfix + ': ' + '\n'.join(numbers_list) + '\nЕсли что-то введено неправильно, нажмите /cost и введите номера заново. Введите текст сообщения:'
        utils.shelve_write(chat_id, states.U_ENT_PHONES)
        numbers_string = ','.join(utils.format_numbers(message.text, '2'))
    except TypeError:
        answer = 'Проверьте правильность введенных номеров'
    bot.send_message(chat_id, answer)
    
@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ENT_PHONES and check_id(message.chat.id), content_types=['text'])
def cost_total(message):
    global numbers_string
    global sending_message
    chat_id = message.chat.id
    text = message.text.replace(' ','+')
    params = {'api_id':config.sms_token, 'to' : numbers_string, 'msg' : text, 'json':1}
    try:
        result = requests.get('https://sms.ru/sms/cost', params)
        if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
            cost = result.json().get('total_cost')
            sms_count = result.json().get('total_sms')
            answer = 'Стоимость отправки <b>%d</b> SMS составит <b>%d р</b>. Чтобы узнать подробности, нажмите /more'%(sms_count, cost)
            utils.shelve_write(chat_id, states.U_ENT_MSG)
            sending_message = message.text
        else:
            answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
    except:
        print(sys.exc_info())
        answer = 'Проверьте правильность введенного сообщения'
    bot.send_message(chat_id, answer, parse_mode='HTML')

@bot.message_handler(commands=['more'], func=lambda message: utils.shelve_read(message.chat.id)==states.U_ENT_MSG and check_id(message.chat.id))
def sms_more_info(message):
    global numbers_string
    global sending_message
    chat_id = message.chat.id
    text = sending_message.replace(' ','+')
    params = {'api_id':config.sms_token, 'to' : numbers_string, 'msg' : text, 'json':1}
    try:
        result = requests.get('https://sms.ru/sms/cost', params)
        if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
            all_sms = result.json().get('sms')
            answer = 'Всего SMS: <b>%s шт</b>;\nОбщая стоимость: <b>%s р</b>;\n==========\n'%(result.json().get('total_sms'), result.json().get('total_cost'))
            for sms in all_sms.items():
                if sms[1].get('status') =='OK':
                    answer = answer + 'Номер получателя: <b>%s</b>;\nСтатус доставки: ОК, сообщение может быть доставлено абоненту;\nКоличество SMS: <b>%s шт</b>;\nСтоимость: <b>%s р.</b>\n==========\n'%(sms[0],sms[1].get('sms'),sms[1].get('cost'))
                else:
                    answer = answer + 'Номер получателя: <b>%s</b>;\nСтатус доставки: <b>%s</b>, <b>%s</b>\n==========\n'%(sms[0],sms[1].get('status'),sms[1].get('status_text'))
            utils.shelve_write(chat_id, states.U_NO_ACT)
        else:
            answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
    except:
        p = sys.exc_info()
        print(p[2])
        answer = 'Проверьте правильность запроса' 
    bot.send_message(chat_id, answer, parse_mode='HTML')
    

@bot.message_handler(func=lambda message: True and check_id(message.chat.id), content_types=['text'])
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
    notifier(30)

