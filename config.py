token = "510378038:AAGMg1dxOJTLciRETnUx4RlrgSWbW34cnfI" #Your bot's token from BotFather
sms_token = 'BA02CA0C-944C-201D-6D3A-3AF3603B9BA3' #token from SMS.RU

admin_ids = ('332761')
public_mode_on = False #True - giving access to anyone, False - reacts on messages only from allowed_ids list
allowed_ids = (admin_ids) #tuple of ids, who may use bot
notify_admins = True #True - send attention message to admin_ids list when someone not allowed trying to use bot

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
