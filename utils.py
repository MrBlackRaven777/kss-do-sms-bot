import config
import sys
import shelve
import re

def shelve_write(id, state):
    with shelve.open(config.shelve_name) as storage:
        storage[str(id)] = state
    
def shelve_read(id):
    with shelve.open(config.shelve_name) as storage:
        try:
            data = storage[str(id)]
        except:
            data = sys.exc_info()
        return data

def format_numbers(string, format='0'):
    number_pattern = re.compile('([\+]?[\(\)\-\d]{9,17})\b*')
    raw_numbers = re.findall(number_pattern, string)
    if len(raw_numbers)==0:
        raise TypeError('must be at least 1 phone number')
    bad_symbols = ['+', '-', '(', ')', ' ']
    clear_numbers = []
    clear_pattern = re.compile('([7-8])([\d]{3})([\d]{3})([\d]{2})([\d]{2})')
    for number in raw_numbers:
        for symb in bad_symbols:
            number = number.replace(symb,'')
        group_number = clear_pattern.match(number)
        g = group_number.groups()
        grouped_number = config.num_format_dict.get(format).format(g[1], g[2], g[3], g[4])
        clear_numbers.append(grouped_number)
    return clear_numbers

def check_id(func_of_bot):
    def wrapper(id)
        if config.public_mode_on = False
            if id in config.a
#def get_request():
#    params = {'api_id':config.sms_token, 'json':1}
#    result = requests.get('https://sms.ru/my/balance', params)
#    if result.json().get('status') == 'OK' and result.json().get('status_code') == 100:
#        balance = int(result.json().get('balance'))
#        answer = 'Ваш баланс: ' + str(balance) + 'р.'
#    else:
#        answer = 'Произошла ошибка №%d: %s'%(result.get('status_code'), result.get('status_text'))
#    bot.send_message(message.chat.id, answer)