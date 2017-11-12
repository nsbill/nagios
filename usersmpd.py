#!/usr/local/bin/python3
import getpass
import sys
import telnetlib
import string
import getopt
import json
import re

#NAS1
HOST1 = "10.77.200.6"
USER1 = 'admin'
PASSWORD1 = 'PASSWD'
PORT1 = '6010'
TIMEOUT = 5
NAS1 = 1

# NAS2
HOST2 = "10.77.200.6"
USER2 = 'admin'
PASSWORD2 = 'PASSWD'
PORT2 = '6005'
TIMEOUT = 5
NAS2 = 2

def nas(host,port,user,password,timeout,json):
    ''' Подключение к NAS серверу по telnet к FreeBSD MPD5 '''
    try:
        tn = telnetlib.Telnet(host,port,timeout)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")
        if json:
            data = []
            for ng in json:
                iface_ng = 'iface ' + ng
                print(iface_ng)
                tn.write(bytes('iface ' + ng + '\n', encoding = 'utf-8'))
                tn.write(b"show customer\n")
#                info = tn.read_until(b"show customer").translate(None, b'\t\v\f\r\'')
                info = tn.read_until(b"show customer").splitlines()
#                print(info)
                data.append(info)
            tn.write(b"exit\n")
        else:
            tn.write(b"show sessions\n")
            tn.write(b"exit\n")
#            data = (tn.read_all().decode('ascii'))
            data = (tn.read_all().decode('utf-8'))
            return data
        return data
    except Exception:
        data = None
        return data

#try:
#    login = sys.argv[1]  # Status Information: проверяем агрумент с nagios
#except Exception:
#    Status = 3
#    print('UNKNOW - Status=%s of user | Status=0' % Status)
##    print('__login__')
#    sys.exit(3)

def check_user(ns_data,nas):
    ''' Выборка пользователей на серверах и парсим результат '''
    if ns_data:
        ii=ns_data.split('\r\n')
        info = []
        for v in ii:
            v = v.split('\t')
            if len(v) == 9:
                info.append(v[0])
        return info

try:
    ns1_data=nas(HOST1,PORT1,USER1,PASSWORD1,TIMEOUT,json=None) # подключаемся к NAS1 
#    print(ns1_data)
    ns2_data=nas(HOST2,PORT2,USER2,PASSWORD2,TIMEOUT,json=None) # подключаемся к NAS2  
#    print(ns2_data)
    if ns1_data == None and ns2_data == None:
        print('ERROR: server are unavailable | %s' % Status)
        sys.exit(2)
    else:
        st1 = check_user(ns1_data,NAS1) # выборка результата с NAS1
#        print(st1)
        st2 = check_user(ns2_data,NAS2) # выборка результата с NAS2 
#        print(st2)
#        ns1_data=nas(HOST1,PORT1,USER1,PASSWORD1,TIMEOUT,json=st1) # подключаемся к NAS1 
#        print(ns1_data)
        ns2_data=nas(HOST2,PORT2,USER2,PASSWORD2,TIMEOUT,json=st2) # подключаемся к NAS2  
#        print(ns2_data)
#        data = str(ns2_data).replace('b\'\\nInterface:\\n','')\
        data = str(ns2_data).replace('b\'\', b\'Interface:\', b\'\\t','')\
                            .replace('\', b\'\\t',',')\
                            .replace('\', b\'',',')\
                            .replace(',\\t',',')\
                            .replace('\'\", b\'',',')\
                            .replace(' show customer\'','')\
                            .replace('seconds','')\
                            .replace('Traffic limits  :\',','')\
                            .replace(' b\"\\t\\tin#1\\t: \'','Traffic limits in#1 : ')\
                            .replace(' b\"\\t\\tout#1\\t: \'','Traffic limits out#1 : ')\
                            .replace('bytes','')\
                            .replace(' b\"\\tPeer ident','Peer ident')\
                            .replace(' b\'\\tSession time ','Session time')\
                            .replace('Multi Session Id:','Multi Session Id :')\
                            .replace('Self addr (name):','Self addr (name) :')\
                            .replace('Peer addr (name):','Peer addr (name) :')\
                            .replace('Peer MAC address:','Peer MAC address :')\
                            .replace('Traffic stats:','Traffic stats : ')\

#                            .split(',')
#        print(data)
        data = data.split('], [')
        print(data)
        log = []
        dictlog = {}
        for val in data:
#            log.append(val.split(','))
            log_ll = []
            log_l = (val.split(','))
            for value in log_l:
                l = value.split(' : ')
                if len(l) == 2:
                    a = re.sub(r'\s+','', l[0])
                    b = l[1]
                    c = [a,b]
                    log_ll.append(c)
#            print(log_ll)
            log.append(dict(log_ll))
        data_json = (json.dumps(log,indent=2, ensure_ascii=False))
        print(data_json)
        with open('users.json', 'w') as outfile:
            json.dump(log, outfile, indent=2, ensure_ascii=False)
#            outfile.write(data_json)
#        sys.exit(0)
#        log = []
#        d = {}
#        for val in data:
##            v = val.replace(' : ',' \' : \' ').split('\\n')
#            v = val.split('\\n')
##            print(type(v))
#            vv = []
#            for value in v:
##            d['aaa'] = v
#                vv.append(value.split(' : '))
##            print(vv)
##            for value in v:
# #               print(value[0:11])
##                d['s'] = value
##                log.append(value.split('\':\''))
##        print(log)
#        print(d)
##        dictionary = dict(log)
##        print(dictionary)
##        data_json = (json.dumps(log,indent=2, ensure_ascii=False))
##        print(data_json)
#
##    st = st1 + st2          # Объеденяем результаты с NAS серверов
##    if len(st) > 1:         # Проверка на кол-во одновременных подключений и подключение
##        print(str(st) + ' | Status=1')
##        sys.exit(2)
##    elif len(st) == 0:
##        print('User is not connected | Status=0')
##        sys.exit(1)
##    else:
##        print(str(st) + ' | Status=1')
##        sys.exit(0)

except Exception: # Когда что не так то все сюда!
    Status = 3
    print('UNKNOW - %s of user | Status=0' % Status)
    sys.exit(3)
