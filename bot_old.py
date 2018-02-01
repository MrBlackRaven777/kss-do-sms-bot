import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
import logging
import requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

upd = Updater(token=config.token)
dsp = upd.dispatcher


def start(bot, upd):
	answer = 'Приветствую тебя, %s! Я бот для управления смс-рассылкой :ООО"КомпозитСпецСтрой". Отправь мне /balance чтобы узнать о текущем состоянии счета.'%(upd.message.from_user.first_name)
	bot.sendMessage(chat_id=upd.message.chat_id, text=answer)

def balance(bot, upd):
    result = requests.get('https://sms.ru/my/balance?api_id=BA02CA0C-944C-201D-6D3A-3AF3603B9BA3&json=1')
    print(result.json())
    if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
        balance = int(result.json().get('balance'))
        answer = 'Ваш баланс: ' + str(balance) + 'р.'
    bot.sendMessage(chat_id=upd.message.chat_id, text=answer)

start_handler = CommandHandler('start', start)
dsp.add_handler(start_handler)
balance_handler = CommandHandler('balance', balance)
dsp.add_handler(balance_handler)

upd.start_polling()
upd.idle()
