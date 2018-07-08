# 生成器可以返回值 return

# 协程
# yield .send():调用方使用send()发送数据
# yield from x, 调用iter(x)从中获得迭代器。但主要功能是打开双向通道，把外层调用方和内层子生成器连接起来

# 调用方
# 委派生成器: 包含yield from <iterable>表达式的生成器函数, 得到的值是子生成器结束时传给StopIteration的第一个参数
# 子生成器: yield from 后面的<iterable>
# 委派生成器暂停后, 调用方将数据发送给子生成器, 子生成器将值发送给调用方, 子生成器结束后, 抛出StopIteration, 委派生成器恢复


def chain(*interables):
    for it in interables:
        yield from it


s = 'ABC'
t = tuple(range(3))
r = list(chain(s, t))
print(r)


from inspect import getgeneratorstate
from collections import namedtuple


def simple_coroutine():
    # 协程定义体中包含yield
    print('-> coroutine start')
    #如果只需从外部获得数据, yield后面不用值(None)
    #产出值后, 协程暂停, 等待赋值
    x = yield 1
    print('-> coroutine recived1: ', x)
    y = yield 1+x
    print('-> coroutine recived1: ', y)
    z = yield 1+y
    print('-> coroutine recived1: ', z)
    #协程结束, 抛出StopIteration


try:
    my_coro = simple_coroutine()
    print(my_coro)
    print(getgeneratorstate(my_coro))
    print('ask for next value')
    # 激活协程, 走到第一个yield
    v = next(my_coro)
    print(getgeneratorstate(my_coro))
    print('get value: ', v)
    print('send value')
    v = my_coro.send(42)
    my_coro.send(43)
    my_coro.close()
    print(getgeneratorstate(my_coro))
    my_coro.send(43)
except StopIteration as ex:
    print(repr(ex))
finally:
    print('end')


class DemoExcption(Exception):
    pass


def averager():
    total = 0.0
    count = 0
    average = 0
    while True:
        try:
            #产出值后, 等待调用方发送值
            term = yield average
            total += term
            count += 1
            average = total/count
        except DemoExcption:
            print('exception handled, continue..')
        else:
            print('recive new value: ', term)
    print('this should new run')


coro_avg = averager()
# 执行到第一个yield
next(coro_avg)
# send()后, 在下一个yield停止, 返回右边的值
v = coro_avg.send(1)
print('get ', v)
v = coro_avg.send(2)
print('get ', v)
v = coro_avg.send(3)
print('get ', v)
v = coro_avg.throw(DemoExcption)
v = coro_avg.send(4)
print('get ', v)


Result = namedtuple('Result', 'count average')


def averager2():
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    #协程结束, 生成器抛出StopIteration异常, 异常对象的value保存返回值
    return Result(count, average)


coro_avg2 = averager2()
next(coro_avg2)

coro_avg2.send(1)
coro_avg2.send(10)
coro_avg2.send(100)
coro_avg2.send(1000)
try:
    coro_avg2.send(None)
except StopIteration as e:
    print(e)


def averager3():
    # 子生成器
    total = 0.0
    count = 0
    average = 0.0
    while True:
        # 调用方发送的值传到term
        term = yield
        print('get ', term)
        if term is None:
            break
        total += term
        count += 1
        average = total/count
    # 协程结束
    return Result(count, average)


def grouper(results, key):
    # 委派生成器: 在yield from暂停, 调用方把数据发送给子生成器
    count = 0
    while True:
        print('do ', key, count)
        count += 1
        #grouper发送的值, 都会传给averager3()
        # averager3返回的Result
        # 传入None后, 子生成器averager中止, 抛出StopIteration异常,
        # 委派生成器恢复运行, 为result[key]赋值
        results[key] = yield from averager3()
        print('get ', results[key])


def grouper2(results, key):
    # 委派生成器: 在yield from暂停, 调用方把数据发送给子生成器
    count = 0
    #grouper发送的值, 都会传给averager3()
    # averager3返回的Result
    print('do ', key)
    try:
        results[key] = yield from averager3()
    except StopIteration as e:
        print('found stopiteration')
        print(e.value)
    count += 1
    print('done ', key, results[key])
    print('do another ')
    # yield
    # noo = yield from averager3()
    #print('done another ', key, noo)


def report(results: dict):
    for k, results in sorted(results.values()):
        print('result: ', k, results)


def doData(data: dict):
    # 调用方
    results = {}
    for key, values in data.items():
        group = grouper2(results, key)
        next(group)
        for v in values:
            print('send ', key, v)
            group.send(v)
        print('send ', key, None)
        group.send(None)
        print('nothing more')
    report(results)


data = {
    'girls;kg': [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m': [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg': [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m': [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}

doData(data)
