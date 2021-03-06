import re
import config
import requests
import json

string = '79267551274, #+79057892429 , 8-963-998-16-15,+7(964)621-52-28 8-(968)-813-47-38 +7-(905)-569-30-84 7 894 584 68 98'
text = 'На объекте Нахимовский 24, стр.1 произошло раскрытие трещины больше допустимого значения. Подробности в эл. письме.'
text = text.replace(' ', '+')

#def format_numbers(string, text):
number_pattern = re.compile('([\+]?[\(\)\-\d]{9,17})\b*')
raw_numbers = re.findall(number_pattern, string)
if len(raw_numbers)==0:
    print('no numbers')
bad_symbols = ['+', '-', '(', ')', ' ']
clear_numbers = []
clear_pattern = re.compile('([7-8])([\d]{3})([\d]{3})([\d]{2})([\d]{2})')
for number in raw_numbers:
    for symb in bad_symbols:
        number = number.replace(symb,'')
    group_number = clear_pattern.match(number)
    g = group_number.groups()
    grouped_number = config.num_format_dict.get('2').format(g[1], g[2], g[3], g[4])
    clear_numbers.append(grouped_number)
    
print(clear_numbers)    
print(','.join(clear_numbers))
params = {'api_id':config.sms_token,'to':','.join(clear_numbers), 'msg':text, 'json':1}
print(params)
result = requests.get('https://sms.ru/sms/cost', params)
print('JSON:\n'+str(result.json()))
print('TOTAL COST: ' + str(result.json().get('total_cost')))
all_sms = result.json().get('sms')
print(all_sms)
for sms in all_sms.items():
    print(sms[0])
    print(sms[1].get('status'))
