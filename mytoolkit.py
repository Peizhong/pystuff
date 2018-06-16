import os
import platform
import socket
import json
import uuid
import hashlib
import time
import functools
# 不可修改
from types import MappingProxyType
from collections import namedtuple, OrderedDict

FileInfo = namedtuple('FileInfo', 'Id Name FullPath UrlPath UpdateTime')

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
    elif curOs == 'Windows':
        if curRealse == '10':
            downloadpath = r'D:/Downloads'
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
    tempDict = {}
    filepath = queryConfig('download')
    fileServer = queryConfig('fileserver')
    for root, _, files in os.walk(filepath):
        for name in files:
            # hidden file
            if name.startswith('.'):
                continue
            fullpath = os.path.join(root, name)
            urlpath = fullpath.replace(filepath, fileServer)
            modifytime = os.path.getmtime(fullpath)
            id = str(uuid.uuid4())
            tempDict[id] = FileInfo(
                id, name, fullpath, urlpath, modifytime)

    downloadfiles = OrderedDict(
        sorted(tempDict.items(), key=lambda t: t[1].UpdateTime))
    return MappingProxyType(downloadfiles)


def getDownloadFileInfo(fid):
    global downloadfiles
    f = downloadfiles.get(fid)
    return f


allFiles = OrderedDict()


def findAllFile(path):
    global allFiles
    allFiles.clear()
    tempDict = {}
    for root, _, files in os.walk(path):
        for name in files:
            # hidden file
            if name.startswith('.'):
                continue
            fullpath = os.path.join(root, name)
            modifytime = os.path.getmtime(fullpath)
            id = str(uuid.uuid4())
            tempDict[id] = FileInfo(id, name, fullpath, '', modifytime)
    allFiles = OrderedDict(
        sorted(tempDict.items(), key=lambda t: t[1].UpdateTime))
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


def getFileMD5(path):
    '''md5'''
    if not os.path.exists(path):
        return ''
    print('file: '+path)
    with open(path, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print('update time: ', os.path.getctime(path))
        print('md5: '+hash)
        return hash


def getBytesLen(string):
    if not isinstance(string, str):
        return -1
    if not string:
        return 0
    return len(string.encode('GBK'))


test_connection = []


def connectivity(source):
    test_connection.append(source)
    print('add->', source)
    return source


@connectivity
def test_mysql():
    import pymysql
    try:
        print('start mysql')
        host = queryConfig('host')
        conn = pymysql.connect(host=host, port=3306,
                               user='root', passwd='mypass', db='MYDEV', charset='utf8')
        cursor = conn.cursor()
        cursor.execute('show tables')
        print(cursor.fetchone())
        cursor.close()
        conn.close()
        print('pass')
        return True
    except Exception as e:
        print(e)
        return False


@connectivity
def test_redis():
    import redis
    try:
        print('start redis')
        host = queryConfig('host')
        r = redis.StrictRedis(host=host, port=6379, db=0)
        r.set('foo', 'bar')
        r.delete('foo')
        print('pass')
        return True
    except Exception as e:
        print(e)
        return False


def testAllConnectivity():
    res = [x() for x in test_connection]


def make_averager():
    '''闭包：函数内部定义函数'''
    count = 0
    total = 0
    # 只有变量：未在本地作用域绑定，即使定义作用域不可用，还是能用
    series = []

    def averager(new_value):
        nonlocal count, total
        series.append(new_value)
        count += 1
        total += new_value
        return total/count
    return averager


def clock(func):
    # 把func属性复制到clocked
    @functools.wraps(func)
    def clocked(*args):
        t0 = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter()-t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked


@clock
def test_nolocal():
    avg = make_averager()
    print(avg(1))
    print(avg(10))


if __name__ == '__main__':
    test_nolocal()
