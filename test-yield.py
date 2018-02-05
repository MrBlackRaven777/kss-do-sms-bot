import telebot
import config
import requests
import re
import utils
from config import u_states as states

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start'])
def start(message):
    answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой ООО"КомпозитСпецСтрой". Отправь мне /balance чтобы узнать о текущем состоянии счета.'%(message.from_user.first_name)
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

@bot.message_handler(func=lambda message: utils.shelve_read(message.chat.id)==states.U_ASK_COST, content_types=['text'])
def cost_phones(message):
    chat_id = message.chat.id
    phone_pattern = re.compile('([\+]?[\(\)\-\d]{9,17})\b*')
    phone_list = re.findall(phone_pattern, message.text)
    print(phone_list)
#    print(re.match(phone_pattern, message.text).group())
    if len(phone_list) > 0:
        answer = 'Вы прислали мне номера: ' + ', '.join(phone_list) + '. Если что-то введено неправильно, нажмите /cost и введите номера заново.
        utils.shelve_write(id=chat_id, state=states.U_ENT_PHONES) 
    else:
        answer = 'Проверьте правильность введенных номеров'
    bot.send_message(chat_id, answer)
     
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo(message):
    answer = 'К сожалению, я не знаю эту команду. Но в будущем я собираюсь расширить свой функционал'
    bot.send_message(message.chat.id, answer)

if __name__ == '__main__':
    bot.polling(none_stop=True)
