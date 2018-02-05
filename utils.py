import config
import sys
import shelve

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