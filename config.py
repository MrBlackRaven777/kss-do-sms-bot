token = "510378038:AAGMg1dxOJTLciRETnUx4RlrgSWbW34cnfI" #Your bot's token from BotFather
sms_token = 'BA02CA0C-944C-201D-6D3A-3AF3603B9BA3'
admin_id = 332761
project_name = 'kss-do-sms-bot'
shelve_name = 'users_states'
phone_num_format_switch = '0'
num_format_dict = {'0' : '+7({0}){1}-{2}-{3}', '1' : '({0}) {1}-{2}{3}', '2' : '7{0}{1}{2}{3}'}
#phone_num_format = num_format_dict.get(phone_num_format_switch)

class u_states:
    U_NO_ACT = '0'
    U_ASK_COST = '1'
    U_ENT_PHONES = '2'
    U_ENT_MSG = '3'
