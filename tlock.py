from threading import Thread, Lock, RLock, Semaphore, Event
import time
mutexA = RLock()
mutexB = RLock()


class MyThread(Thread):
    def run(self):
        self.func1()
        self.func2()

    def func1(self):
        mutexA.acquire()
        print('\033[41m%s 拿到A锁\033[0m' % self.name)

        mutexB.acquire()
        print('\033[42m%s 拿到B锁\033[0m' % self.name)
        mutexB.release()
        print('\033[42m%s 释放B锁\033[0m' % self.name)

        mutexA.release()
        print('\033[42m%s 释放A锁\033[0m' % self.name)

    def func2(self):
        mutexB.acquire()
        print('\033[43m%s 拿到B锁\033[0m' % self.name)
        time.sleep(.1)

        mutexA.acquire()
        print('\033[44m%s 拿到A锁\033[0m' % self.name)

        mutexA.release()
        print('\033[42m%s 释放A锁\033[0m' % self.name)

        mutexB.release()
        print('\033[42m%s 释放B锁\033[0m' % self.name)


if __name__ == '__main__':
    for i in range(10):
        t = MyThread()
        t.start()
