import re
import config

string = '79267551274, +79057892429 , 8-963-998-16-15,+7(964)621-52-28 8-(968)-813-47-38 +7-(905)-569-30-84 7 894 584 68 98'
def format_numbers(string)
    number_pattern = re.compile('([\+]?[\(\)\-\d]{9,17})\b*')
    raw_numbers = re.findall(number_pattern, string)
    if len(raw_numbers)==0:
        return 'no numbers'
    bad_symbols = ['+', '-', '(', ')', ' ']
    clear_numbers = []
    clear_pattern = re.compile('([7-8])([\d]{3})([\d]{3})([\d]{2})([\d]{2})')
    for number in raw_numbers:
        for symb in bad_symbols:
            number = number.replace(symb,'')
        group_number = clear_pattern.match(number)
        g = group_number.groups()
        grouped_number = config.phone_num_format.format(g[1], g[2], g[3], g[4])
        clear_numbers.apppend(grouped_number)
    return clear_numbers
