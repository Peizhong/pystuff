import time


def consumer_work(len):
    # 读取send传进的数据，并模拟进行处理数据
    print("writer:")
    w = ''
    while True:
        w = yield w
        # w接收send传进的数据,同时也是返回的数据
        print('[CONSUMER] Consuming %s...>> ', w)
        w *= len
        # 将返回的数据乘以100
        time.sleep(0.1)


def consumer(coro):
    # 将数据传递到协程(生成器)对象中
    v = yield from coro
    print('consumer ', v)


def produce(c):
    next(c)
    for i in range(5):
        print('[Produce] Producing %s----', i)
        w = c.send(i)  # 发送完成后进入协程中执行
        print('[Produce] receive %s----', w)
    print('close')
    c.close()


c1 = consumer_work(100)
produce(consumer(c1))


def gen(subgen):
    # subgen获得控制权，产出的值传给调用方，gen阻塞等待subgen中止
    yield from subgen


def subgen():
    yield x


def htest():
    i = 1
    while True:
        n = yield i
        print('recive ', n)
        if i == 3:
            pass
            # return 100
        i += 1


def itest():
    val = yield from htest()
    print(val)


t = itest()
t.send(None)
j = 0
while j < 3:
    j += 1
    try:
        print('send ', j)
        v = t.send(j)
        print('back ', v)
    except StopIteration as e:
        print('异常了')
t.send(3)
t.send(5)
t.close()


flags = ('china', 'uk', 'usa', 'new zealand', 'peru')


def downloadFlag():
    path = None
    while True:
        name = yield path
        print('get {} to download'.format(name))
        time.sleep(.5)
        path = 'downloads/%r' % name


def transfer(coro):
    yield from coro


def starter():
    downcoro = downloadFlag()
    next(downcoro)
    for f in flags:
        print('send ', f)
        p = downcoro.send(f)
        print('get ', p)
    downcoro.close()
    print('end game')


starter()
