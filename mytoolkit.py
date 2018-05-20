import os
import platform
import socket
import json
from urllib import parse
from collections import namedtuple

FileInfo = namedtuple('FileInfo', 'Name UrlPath')

curOs = platform.system()
print('current os is '+curOs)
curRealse = platform.release()
print('current release is '+curRealse)

localconfig = {}


def makeDir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        return False


def getDownloadPath(subFolder=''):
    if curOs == "Darwin":
        downloadpath = r'/Users/Peizhong/Downloads'
    elif curOs == "Linux":
        hostname = socket.gethostname()
        if 'raspberry' in hostname:
            downloadpath = r'/home/pi/downloads'
        else:
            downloadpath = r'/home/peizhong/downloads'
    else:
        downloadpath = r'E:/Downloads'
    if subFolder:
        downloadpath = os.path.join(downloadpath, subFolder)
    makeDir(downloadpath)
    return downloadpath


def getFileServer():
    if curOs == "Darwin":
        serverpath = r'http://192.168.3.172/downloads/'
    elif curOs == "Linux":
        hostname = socket.gethostname()
        if 'raspberry' in hostname:
            serverpath = r'http://192.168.3.172/downloads/'
        else:
            serverpath = r'http://193.112.41.28/downloads/'
    else:
        serverpath = r'localhost'
    return serverpath


def findAllFile(filepath=''):
    if not filepath:
        filepath = queryConfig('download')
    fileServer = queryConfig('fileserver')
    headindex = len(filepath)+1
    selectedFiles = []
    for root, _, files in os.walk(filepath):
        for name in files:
            # hidden file
            if name.startswith('.'):
                continue
            fixName = name
            header = root[headindex:]
            if header:
                fixName = '%s||%s' % (header, name)
            refName = '%s/%s' % (header, name)
            selectedFiles.append(
                FileInfo(fixName, fileServer+parse.quote(refName)))
    return selectedFiles


def queryConfig(name):
    global localconfig
    if not localconfig:
        localconfig = readConfig()
    if name in localconfig:
        return localconfig[name]
    return ''


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
            if 'download' not in config:
                config['download'] = getDownloadPath()
            if 'fileserver' not in config:
                config['fileserver'] = getFileServer()
            if 'avmtdb' not in config:
                config['avmtdb'] = os.path.join(config['download'], 'avmt.db')
    else:
        host = getHost()
        config = {
            'host': getHost(),
            'database': databaseConfig(host),
            'download': getDownloadPath(),
            'fileserver': getFileServer(),
            'avmtdb': os.path.join(config['download'], 'avmt.db')
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
