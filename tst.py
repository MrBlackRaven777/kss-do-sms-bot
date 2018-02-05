import re

string = '79267551274, +79057892429 , 8-963-998-16-15,+7(964)621-52-28 8-(968)-813-47-38 +7-(905)-569-30-84 7 894 584 68 98'
phone_pattern = re.compile('([\+]?[\(\)\-\d]{9,17})\b*')
phone_list = re.findall(phone_pattern, string)
print(phone_list)
bad_symbols = ['+', '-', '(', ')', ' ']
clear_phones = []
clear_pattern = re.compile('([7-8])([\d]{3})([\d]{3})([\d]{2})([\d]{2})')
for phone in phone_list:
    for symb in bad_symbols:
        phone = phone.replace(symb,'')
    group_number = clear_pattern.match(phone)
    grouped_nember = '('+ str(group_number.group(1)) + ') ' + str(group_number.group(2)) + '-' + str(group_number.group(3,4))
    print(group_number)
    clear_phones.append(group_number)
print(clear_phones)