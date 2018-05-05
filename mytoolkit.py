import os
import platform
import socket
import json


localconfig = {}


def queryConfig(name):
    global localconfig
    if not localconfig:
        localconfig = readConfig()
    if name in localconfig:
        return localconfig[name]
    return ''


def getDownloadPath():
    curOs = platform.system()
    print('current os is '+curOs)
    curRealse = platform.release()
    print('current release is '+curRealse)
    if curOs == "Darwin":
        downloadpath = r'/Users/Peizhong/Downloads'
    elif curOs == "Linux":
        downloadpath = r'/home/peizhong/downloads'
    else:
        downloadpath = r'E:/Downloads'
    return downloadpath


def readConfig():
    configpath = 'localconfig.json'
    config = {}
    if os.path.exists(configpath):
        with open(configpath, 'r') as read_f:
            config = json.load(read_f)
            if 'host' not in config:
                config['host'] = getHost()
            if 'database' not in config:
                config['database'] = databaseConfig(config['host'])
    else:
        host = getHost()
        config = {
            'host': host,
            'database': databaseConfig(host)
        }
    # 不管有没有改数据，都写一遍
    with open(configpath, "w") as write_f:
        json.dump(config, write_f)
    print('using config: ')
    print(config)
    return config


def getHost():
    #ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    #addrs = socket.getaddrinfo(socket.gethostname(), None)
    host = input("input host's ip (default is %s): " % ip)
    if not host:
        return ip
    return host


def databaseConfig(host, dbflag=1):
    if dbflag == 2:
        return sqliteConfig()
    else:
        return mysqlConfig(host)


def mysqlConfig(host):
    username = input("input mysql's user name: ")
    password = input("input mysql's password: ")
    return {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'MYDEV',
        'USER': username,
        'PASSWORD': password,
        'HOST': host,   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }


def sqliteConfig():
    return {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
