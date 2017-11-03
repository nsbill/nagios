#!/usr/local/bin/python3
import getpass
import sys
import telnetlib
import string
import getopt

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

def nas(host,port,user,password,timeout):
    ''' Подключение к NAS серверу по telnet к FreeBSD MPD5 '''
    try:
        tn = telnetlib.Telnet(host,port,timeout)
        tn.read_until(b"Username: ")
        tn.write(user.encode('ascii') + b"\n")
        if password:
            tn.read_until(b"Password: ")
            tn.write(password.encode('ascii') + b"\n")

        tn.write(b"show sessions\n")
        tn.write(b"exit\n")
        data = (tn.read_all().decode('ascii'))
        return data
    except Exception:
        data = None
        return data

try:
    login = sys.argv[1]  # проверяем агрумент с nagios
except Exception:
    Status = 3
    print('UNKNOW - Status=%s of user' % Status)
    print('__login__')
    sys.exit(3)

def check_user(ns_data,nas,login=None):
    ''' Проверяем пользователя на серверах и парсим результат '''
    if ns_data:
        ii=ns_data.split('\r\n')
        info = []
        for v in ii:
            v = v.split('\t')
            if len(v) == 9:
                v = (dict(zip(('ng','ip',3,4,'vlan',6,7,'user','mac','nas'),v)))
                info.append(v)
        up = []
        for value in info:
            if value.get('user') == login: # Проверка подключен пользователь на сервере
#            Status = 0
                up.append((nas, value.get('ng'), value.get('ip'), value.get('mac'), value.get('vlan')))
        return up
    else:
        up = []
        return up

try:
    ns1_data=nas(HOST1,PORT1,USER1,PASSWORD1,TIMEOUT) # подключаемся к NAS1 
#    print(ns1_data)
    ns2_data=nas(HOST2,PORT2,USER2,PASSWORD2,TIMEOUT) # подключаемся к NAS2  
#    print(ns2_data)
    if ns1_data == None and ns2_data == None:
        print('ERROR: server are unavailable')
        sys.exit(2)
    else:
        st1 = check_user(ns1_data,NAS1,login) # выборка результата с NAS1
#        print(st1)
        st2 = check_user(ns2_data,NAS2,login) # выборка результата с NAS2 
#        print(st2)

    st = st1 + st2          # Объеденяем результаты с NAS серверов
    if len(st) > 1:         # Проверка на кол-во одновременных подключений и подключение
        print(st)
        sys.exit(2)
    elif len(st) == 0:
        print('User is not connected')
        sys.exit(1)
    else:
        print(st)
        sys.exit(0)

except Exception: # Когда что не так то все сюда!
    Status = 3
    print('UNKNOW - %s of user' % Status)
    sys.exit(3)
