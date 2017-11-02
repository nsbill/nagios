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

# NAS2
HOST2 = "10.77.200.6"
USER2 = 'admin'
PASSWORD2 = 'PASSWD'
PORT2 = '6005'

#def usage():
#    print ("""Usage: check_usermpd [-h|--help] [-login|--login]"
#    User Online""")
#    sys.exit(3)
#print(sys.argv)

def getUsers():
    ''' Online user '''
    sys.exit(3)
#print(sys.argv[1])

def nas(host,port,user,password):
    tn = telnetlib.Telnet(host,port)
    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    tn.write(b"show sessions\n")
    tn.write(b"exit\n")
    data = (tn.read_all().decode('ascii'))
    return data

try:
    login = sys.argv[1]
except Exception:
    Status = 3
    print('UNKNOW - Status=%s of user' % Status)
    sys.exit(3)

def check_user(ns_data,login=None):
    ii=ns_data.split('\r\n')
    info = []
    for v in ii:
        v = v.split('\t')
        if len(v) == 9:
            v = (dict(zip(('ng','ip',3,'vlan',5,6,7,'user','mac'),v)))
            info.append(v)
    for value in info:
#        print('===LOGIN = %s ===' % login)
        if value.get('user') == login:
#            Status = 0
            print('Connection is UP - %s of user' % login)
            return sys.exit(0)
#    Status = 1
    print('Connection is DOWN - %s of user' % login)
    return sys.exit(1)

try:
    ns1_data=nas(HOST1,PORT1,USER1,PASSWORD1)
    ns2_data=nas(HOST2,PORT2,USER2,PASSWORD2)
#    st1 = check_user(ns1_data,login)
    st2 = check_user(ns2_data,login)
except Exception:
#        return Status
    Status = 3
    print('UNKNOW - %s of user' % Status)
    sys.exit(3)
