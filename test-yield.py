import telebot
import config
import requests
import re
import utils
from config import u_states as states

bot = telebot.TeleBot('345248007:AAF4R8mKESAnqBn_jXOReMLbatqMzz8TMwc')

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


@bot.message_handler(func=lambda message: check_id(message.chat.id), commands=['start'])
def start(message):
    answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой ООО"КомпозитСпецСтрой". Отправь мне /balance чтобы узнать о текущем состоянии счета.'%(message.from_user.first_name)
    bot.send_message(message.chat.id, answer)




#@bot.message_handler(commands=['start'])
#def start(message):
#    answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой ООО"КомпозитСпецСтрой". Отправь мне /balance чтобы узнать о текущем состоянии счета.'%(message.from_user.first_name)
#    bot.send_message(message.chat.id, answer)
#
@bot.message_handler(func=lambda message: check_id(message.chat.id), commands=['balance'])
def balance(message):
    params = {'api_id':config.sms_token, 'json':1}
    result = requests.get('https://sms.ru/my/balance', params)
    if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
        balance = int(result.json().get('balance'))
        answer = 'Ваш баланс: ' + str(balance) + 'р.'
    else:
        answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
    bot.send_message(message.chat.id, answer)
#    
@bot.message_handler(func=lambda message: check_id(message.chat.id), commands=['cost'])
def cost_start(message):
    chat_id = message.chat.id
    utils.shelve_write(id=chat_id, state=states.U_ASK_COST)
    answer = 'Введите список номеров для проверки стоимости. Все номера должны быть в одном сообщении, в теле номера не должно быть пробелов.'
    bot.send_message(chat_id, answer)
#
#@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ASK_COST, content_types=['text'])
#def cost_phones(message):
#    chat_id = message.chat.id
#    try:
#        numbers_list = utils.format_numbers(message.text)
#        answer = 'Вы прислали мне номера: ' + ', '.join(numbers_list) + '. Если что-то введено неправильно, нажмите /cost и введите номера заново.
#    except 'error':
#        answer = 'Проверьте правильность введенных номеров'
#    bot.send_message(chat_id, answer)
#     
#    
@bot.message_handler(content_types=['text'], func=lambda message: check_id(message.chat.id))
def echo(message):
    answer = 'К сожалению, я не знаю эту команду. Но в будущем я собираюсь расширить свой функционал'
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.polling(none_stop=True)
