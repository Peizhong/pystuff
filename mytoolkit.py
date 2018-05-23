import os
import platform
import socket
import json
import uuid
# 不可修改
from types import MappingProxyType
from collections import namedtuple, OrderedDict

FileInfo = namedtuple('FileInfo', 'Id Name FullPath UrlPath')

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
        downloadpath = r'/Volumes/Downloads'
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


downloadfiles = OrderedDict()


def findAllDownloadFile():
    global downloadfiles
    downloadfiles.clear()
    filepath = queryConfig('download')
    fileServer = queryConfig('fileserver')
    for root, _, files in os.walk(filepath):
        for name in files:
            # hidden file
            if name.startswith('.'):
                continue
            fullpath = os.path.join(root, name)
            urlpath = fullpath.replace(filepath, fileServer)

            id = str(uuid.uuid4())
            downloadfiles[id] = FileInfo(id, name, fullpath, urlpath)
    return MappingProxyType(downloadfiles)


def getDownloadFileInfo(fid):
    global downloadfiles
    f = downloadfiles.get(fid)
    return f


allFiles = OrderedDict()


def findAllFile(path):
    global allFiles
    allFiles.clear()
    for root, _, files in os.walk(path):
        for name in files:
            # hidden file
            if name.startswith('.'):
                continue
            fullpath = os.path.join(root, name)
            id = str(uuid.uuid4())
            allFiles[id] = FileInfo(id, name, fullpath, '')
    return MappingProxyType(allFiles)


def getFileInfo(fid):
    global allFiles
    f = allFiles.get(fid)
    return f


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
        print('read local file')
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
            if 'emailaccount' not in config:
                config['emailaccount'] = getAnswer('Email account')
            if 'emailpasswd' not in config:
                config['emailpasswd'] = getAnswer('Email password')
            if 'avmtdb' not in config:
                config['avmtdb'] = os.path.join(config['download'], 'avmt.db')
    else:
        host = getHost()
        config = {
            'host': getHost(),
            'database': databaseConfig(host),
            'download': getDownloadPath(),
            'fileserver': getFileServer(),
            'emailaccount': getAnswer('Email account'),
            'emailpasswd': getAnswer('Email password'),
            'avmtdb': os.path.join(config['download'], 'avmt.db')
        }
    # 不管有没有改数据，都写一遍
    with open(configpath, "w") as write_f:
        json.dump(config, write_f)
    print('using config: ')
    print(config)
    return config


def getHost():
    # ip = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    # addrs = socket.getaddrinfo(socket.gethostname(), None)
    host = input("input host's ip (default is %s): " % ip)
    if not host:
        return ip
    return host


def getAnswer(question):
    while True:
        answer = input('input the %s: ' % question)
        if answer:
            return answer
        print('please try again')


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
