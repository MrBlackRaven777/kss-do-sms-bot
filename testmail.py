from exchangelib import Account, Credentials
import re
import shelve
import time

credentials = Credentials('d.voskresenskiy@kss.do', 'kSSDO111')
account = Account('d.voskresenskiy@kss.do', credentials=credentials, autodiscover=True)

#for item in account.inbox.unread():
#    print(item)
#
def notifier(delay):
    with shelve.open('nodes') as nodes_storage:
        nodes_dict = dict(nodes_storage)
        
    discharged = account.inbox / 'MeshLogic' / 'Разряжаются'
    if discharged.unread_count > 0:
        pattern = re.compile('([_\d]{7,9}).*([,\d]{5}).*(\d{2}\.\d{2}\.\d{4}).*(\d{2}\:\d{2}\:\d{2}).*([0-9,]{5}).*(\d{2}\.\d{2}\.\d{4}).*(\d{2}\:\d{2}\:\d{2})', re.DOTALL)
        for item in discharged.filter(is_read=False):
#            print(item.body)
            r = re.findall(pattern, item.body)
            print(r)
            print(r[0][0])
            node = str(r[0][0])[:str(r[0][0]).find('_')]
            print(node)
            msg = 'Оповещение Нахимовский:\n%s в %s узел %s (У%s) разрядился до %sВ'%(r[0][2], r[0][3], node, nodes_dict.get(node), r[0][1])
            print(msg)
            print(item.is_read)
            item.is_read = True
            item.save
    del nodes_dict
    time.sleep(delay)
    notifier(delay)
    
notifier(900)
# directory('Inbox').order_by('-datetime_received')[:10]:
#    print(item.subject, item.sender, item.datetime_received)


#with open('nodes.txt', 'r') as nodes:
#    pat = re.compile('([\d]{4,6})\s*У(\d+)')
#    for line in nodes.readlines():
#        print(line)
#        res = re.findall(pat, line)
#        print(res[0][0])
#        with shelve.open('nodes') as storage:
#            storage[res[0][0]] = res[0][1]