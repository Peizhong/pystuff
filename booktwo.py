# 网络编程
from socket import socket, AF_INET, SOCK_STREAM
from time import sleep, ctime
from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
import threading
from threading import Thread, Lock, current_thread, BoundedSemaphore
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from atexit import register
from re import compile
from urllib import parse, request
from random import randrange, randint
import tkinter
import sqlite3

HOST = ''
PORT = 21567
BUFSIZE = 1024
ADDR = (HOST, PORT)


def StartServer():
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)

    while True:
        print('waiting for connection...')
        tcpCliSock, addr = tcpSerSock.accept()
        print('...connected from: %s:%d' % addr)
        while True:
            data = tcpCliSock.recv(BUFSIZE)
            if not data:
                break
            recv = data.decode('utf-8')
            rlpy = '[%s] %s' % (ctime(), recv)
            print('send %s to client' % (rlpy))
            tcpCliSock.send(bytes(rlpy, 'utf-8'))
        tcpCliSock.close()
    tcpSerSock.close()


class MyRequestHandler(SRH):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())


def StartLibServer():
    tcpServ = TCP(ADDR, MyRequestHandler)
    print('waiting for connection...')
    tcpServ.serve_forever()


def StartClient():
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    while True:
        data = input('>')
        if not data:
            break
        tcpCliSock.send(bytes(data, 'utf-8'))
        data = tcpCliSock.recv(BUFSIZE)
        if not data:
            break
        print(data.decode('utf-8'))
    tcpCliSock.close()


def loop(nloop, nsec):
    print('start loop %s at %s' % (nloop, ctime()))
    sleep(nsec)
    print('loop done at %s' % (ctime()))


def doThread():
    print('start do thread at %s' % (ctime()))
    loops = [4, 2]
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=loop, args=(i, loops[i]))
        threads.append(t)
    # start thread
    for i in nloops:
        threads[i].start()
    for i in nloops:
        threads[i].join()
    print('all don at %s' % (ctime()))


def alwaysPrint(nsec=1):
    while True:
        print('this is thread printing stuff at '+ctime())
        sleep(nsec)


def printStuffAndServer():
    threads = []
    thread1 = threading.Thread(target=alwaysPrint, args=(2,), name='justprint')
    threads.append(thread1)
    # threading 支持守护进程
    # 实例化后不会立即执行
    thread2 = threading.Thread(target=StartServer, name='server')
    threads.append(thread2)
    # 通过调用每个线程的start()开始执行
    for thread in threads:
        thread.start()
    # join()方法等待线程结束
    for thread in threads:
        thread.join()


class ThreadFunc(object):
    def __init__(self, func, args, name=""):
        self.name = name
        self.func = func
        self.args = args

    def __call__(self):
        "调用函数的实例"
        # 储存类的参数，传给函数
        self.func(*self.args)


def TestFuncTread():
    loops = [4, 2]
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = threading.Thread(target=ThreadFunc(
            loop, (i, loops[i]), loop.__name__))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print('all done')


class MyThread(threading.Thread):
    def __init__(self, func, args, name=""):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)


def TestMyThread():
    loops = [4, 2]
    threads = []
    nloop = range(len(loops))
    for i in nloop:
        t = MyThread(loop, (i, loops[i]), loop.__name__)
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print('all done')


REGEX = compile(r'百度为您找到相关结果约([\d,]+)个')
BAIDU = r'http://www.baidu.com/s?'


def getRanking(isbn):
    queryDict = {
        "wd": isbn
    }
    url = '%s%s' % (BAIDU, parse.urlencode(queryDict))
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    req = request.Request(url, headers=header)
    page = request.urlopen(req)
    data = page.read()
    decode = data.decode('utf-8')
    page.close()
    res = REGEX.findall(decode)
    if not res:
        return "0"
    return res[0]


def showRanking(query):
    rank = getRanking(query)
    print('找到 %s 个关于[%s]结果' % (rank, query))


def showRankingThread(query, threads):
    t = threading.Thread(target=showRanking, args=(query,))
    threads.append(t)
    t.start()


def multiThreadQuery():
    questions = ['wang', '培', 'zhong', 'python', 'c#']
    threads = []
    for query in questions:
        showRankingThread(query, threads)
    for thread in threads:
        thread.join()
    print('join complete at '+ctime())


def poolTreadQuery():
    questions = ['wang', '培', 'zhong', 'python', 'c#']
    with ThreadPoolExecutor(3) as exexcutor:
        # zip: 打包为元组的列表, 长度为最短的
        for q, ranking in zip(questions, exexcutor.map(getRanking, questions)):
            print('- %s count: %s' % (q, ranking))
    print('wtf, it''s done')


class CleanOutputSet(set):
    def __str__(self):
        "默认输出"
        return ', '.join(x for x in self)


remaining = CleanOutputSet()

lock = Lock()


def lockloop(nsec):
    "锁"
    myname = current_thread().name
    with lock:
        remaining.add(myname)
        print('%s start thread %s' % (ctime(), myname))
    sleep(nsec)
    with lock:
        remaining.remove(myname)
        print('%s complete %s (%s secs)' % (ctime(), myname, nsec))
        print('remaining: %s' % (remaining or 'None'))


def testLock():
    # 生成随机长度为[3,7]的范围为[2,5]的随机数
    loops = (randrange(2, 5) for x in range(randrange(3, 7)))
    for pause in loops:
        Thread(target=lockloop, args=(pause,)).start()


candyTray = BoundedSemaphore(5)


def refillCandy():
    with lock:
        print('refill candy...')
        try:
            candyTray.release()
        except ValueError:
            print('\tfull, skipping')
        else:
            print('\tadded candy')


def buyCandy():
    with lock:
        print('buying candy...')
        if candyTray.acquire(False):
            print('\tgot one')
        else:
            print('\t:( no candy')


def producer(loop):
    while True:
        refillCandy()
        sleep(randrange(loop))


def customer(loop):
    while True:
        buyCandy()
        sleep(randrange(loop))


def testBound():
    nloops = randrange(2, 6)
    print('candy machine is full at ' + ctime())
    Thread(target=customer, args=(randrange(nloops, nloops+2),)).start()
    Thread(target=producer, args=(nloops,)).start()


def writeQ(queue):
    print('producting object for Q...')
    queue.put('xxx', 1)
    print('\tnow queue size is %d' % (queue.qsize()))


def readQ(queue):
    val = queue.get(1)
    print('consumed object from Q... size now is %d' % (queue.qsize()))


def reader(queue, loops):
    for i in range(loops):
        readQ(queue)
        sleep(randint(3, 5))


def writer(queue, loops):
    for i in range(loops):
        writeQ(queue)
        sleep(randint(1, 3))


funcs = [writer, reader]
nFuncs = range(len(funcs))


def testQue():
    print('hello this is queue')
    q = Queue(32)
    nloops = randint(2, 5)
    print('w/r will run %d times' % (nloops))
    threads = []
    for i in nFuncs:
        i = MyThread(funcs[i], (q, nloops), funcs[i].__name__)
        threads.append(i)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print('queue all done')


def doUI():
    root = tkinter.Tk()
    root.minsize(240, 320)
    root.maxsize(380, 530)
    root.title('This is PYTHON')
    label = tkinter.Label(root, text='nihao')
    label.pack()
    btnQuit = tkinter.Button(root, text='退出', command=root.quit)
    btnQuit.pack(fill=tkinter.X, expand=1)
    root.mainloop()


def doDatabase():
    cxn = sqlite3.connect('db.sqlite3')
    cur = cxn.cursor()
    cur.execute('select * from learning_logs_entry')
    for entry in cur.fetchall():
        print(entry)
    cur.close()
    cxn.commit()
    cxn.close()


def _main():
    print('hello: '+ctime())
    doDatabase()


@register
def _atexit():
    # 脚本退出前执行这个函数
    print('script end at '+ctime())


if __name__ == '__main__':
    _main()

"""
TestMyThread()
TestFuncTread()
printStuffAndServer()

print("select start type:")
print('1. Server')
print('2. lib Server')
print('3. Client')
cs = int(input('what do you want?'))
if cs == 1:
    StartServer()
elif cs == 2:
    StartLibServer()
elif cs == 3:
    StartClient()
else:
    print('bye')
"""
