# asyncio: 事件驱动的协程
# 多线程和异步的区别
# 异步编程，回调和协程

import threading
import asyncio
import itertools
import time
import sys


class Singal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char+' '+msg
        write(status)
        flush()
        # 退格
        write('\x08'*len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' '*len(status)+'\x08'*len(status))


def slow_function():
    '耗时的操作'
    time.sleep(3)
    return 43


def spinner_thread():
    '''线程方式'''
    singal = Singal()
    # Thread对象用于调用可调用的对象
    spinner = threading.Thread(target=spin, args=('thinking!', singal))
    print('spinner object: ', spinner)
    # Thread对象要调用start()
    spinner.start()
    result = slow_function()
    singal.go = False
    spinner.join()
    return result


@asyncio.coroutine
def spin_asyncio(msg):
    # 交给ayncio处理的协程使用@asyncio.coroutine装饰
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char+' '+msg
        write(status)
        flush()
        # 退格
        write('\x08'*len(status))
        try:
            # 休眠，但不会阻塞事件循环
            yield from asyncio.sleep(.1)
        except asyncio.CancelledError:
            # 发出取消请求，spin_asyncio苏醒后抛出异常
            break
    write(' '*len(status)+'\x08'*len(status))


@asyncio.coroutine
def slow_function_asyncio():
    # 协程函数，假装进行io操作
    # yield from 把控制权交给主循环
    yield from asyncio.sleep(3)
    return 42


@asyncio.coroutine
def supervisor_asyncio():
    # 排定spin_asyncio运行，包装成Task对象
    # Task对象用户驱动协程，
    spinner = asyncio.async(spin_asyncio('think!'))
    print('spinner object: ', spinner)
    result = yield from slow_function_asyncio()
    spinner.cancel()
    return result


def main_asyncio():
    # 事件的循环引用
    loop = asyncio.get_event_loop()
    # 驱动协程，让其运行完毕
    result = loop.run_until_complete(supervisor_asyncio())
    loop.close()
    print('done')


def main():
    result = spinner_thread()
    print('done')


if __name__ == '__main__':
    main_asyncio()
