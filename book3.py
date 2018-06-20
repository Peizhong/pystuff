# 流畅的python: 介绍python3的特性
import collections

import re

from random import randrange, randint, choice

from math import hypot

from array import array
from random import random

import time

import functools

import html

import numbers

import copy

# 纸牌类：少数属性，没有方法的对象
Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDesk:
    "隐式继承了object类，但功能没有继承。通过实现特殊方法，使其能用于标准库"
    # 特殊方法是给解释器用的，不用调用

    # 公共的类属性
    # 转换成列表
    ranks = [str(s) for s in range(2, 10)]+list('JQKA')
    # 按空格分割
    suits = 'spades hearts diamonds clubs'.split()

    def __init__(self):
        # 两个for：笛卡尔积
        self.cards = [Card(rank, suit)
                      for rank in self.ranks for suit in self.suits]

    # 实现特殊方法来利用Python数据模型
    def __len__(self):
        "len(FrenchDesk)"
        return len(self.cards)

    # 如果没有__contains__, 用迭代搜索
    def __getitem__(self, position):
        "处理FrenchDesk[],变成可迭代"
        return self.cards[position]


suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDesk.ranks.index(card.rank)
    return rank_value*len(suit_values)+suit_values[card.suit]


l = [1, 3, 5, 7, 9, 11, 13, 15]
# [x,y,z] z:方向/步长，如果为负，从最后开始
l1 = l[:6:-2]
l1 = l[4::-2]


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        "把对象用字符串表示,%r标准输出"
        return "Vector(%r,%r)" % (self.x, self.y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        "bool()先尝试__bool__, 再用__len__"
        return bool(abs(self))

    def __add__(self, other):
        x = self.x + other.x
        y = self.x + other.y
        return Vector(x, y)

    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)

# 容器序列：对象的引用：list, tuple, collection.deque
# 扁平序列：对象的值：str,bytes
# 可变序列 不可变序列


# 列表推导
symbols = '!@#$%^&*'
codes = [ord(x) for x in symbols]
# 代替filter
beyond_ascii = [ord(x) for x in symbols if ord(x) > 127]
# 生成器表达式：逐个产出元素

# 平行赋值
a, b, *rest = range(5)
a, *rest, b = range(5)

# 嵌套元组
metro_areas = [('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
               ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
               ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
               ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
               ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)), ]
for name, cc, pop, (latitude, longitude) in metro_areas:
    print('%r,%r' % (latitude, longitude))


LatLong = collections.namedtuple('Latong', 'lat long')
# LatLong = collections.namedtuple('LatLong',['lat','long'])
City = collections.namedtuple('City', 'Name Province Country Location')
shenzhen = City._make(('Shenzhen', 'Guangdong', 'China', LatLong(112, 24)))
for key, value in shenzhen._asdict().items():
    print('%r-%r' % (key, value))

l = list(range(10))
l[2:5] = [20, 30]
del l[5:7]

# 列表的列表
three = [['_']*3 for x in range(3)]
three[2][1] = 'x'
print(three)

# array


def doArray():
    floats = array('d', (random() for i in range(10**7)))
    with open('floats.bin', 'wb') as fp:
        floats.tofile(fp)
    print(floats[-1])

    floats2 = array('d')
    with open('floats.bin', 'rb') as fp:
        floats2.fromfile(fp, 10**7)
    print(floats2[-1])


def doQueue():
    "双向队列"
    dq = collections.deque(range(10), maxlen=10)
    # 从尾部取n值插到头部
    dq.rotate(3)
    # 从头部取n值插到尾部
    dq.rotate(4)
    # appendleft, extend


def readBook():
    word_re = re.compile(r'\w+')
    index = {}
    with open('booktwo.py', encoding='utf-8') as fp:
        for line_no, line in enumerate(fp, 1):
            for match in word_re.finditer(line):
                word = match.group().lower()
                column_no = match.start()+1
                location = (line_no, column_no)
                # 自动处理不存在的key
                index.setdefault(word, []).append(location)
    for word in sorted(index, key=str.upper):
        print(word, index[word])


def doSet():
    l1 = ['a', 'b', 'c', 'a', 'b']
    l2 = ['b', 'c', '1', '2']
    s = set(l1)
    s2 = set(l2)
    # 两个集合共有的
    l = len(s2 & s)
    # 字面量：不用构造
    l1 = {1, 2, 3, 3, 4, 4, 5, 5}
    # 字典和集合，散列，消耗内容，告诉判断元素是否存在
    # hash(search_key)根据散列值查找:先用部分数字查找数据


def doFunc():
    '''一等对象'''
    # 能赋给变量、能作为参数传给函数、能作为函数返回结果
    # 高阶函数：接受函数作为参数，或返回函数：如map,filter=>用列表推导代替[ for x in ]
    # 匿名函数 lambda


def doTag(name, *content, cls=None, **attrs):
    '''生成html标签'''
    if cls:
        attrs['class'] = cls
    if attrs:
        attrs_str = ' '.join('%s="%s"' % (attr, value)
                             for attr, value in sorted(attrs.items()))
    else:
        attrs_str = ' '
    if content:
        return '\n'.join('<%s%s>%s</%s>' % (name, attrs_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attrs_str)


def clip(text: str, max_len: 'int > 0'=80) -> str:
    '''注释'''
    end = None
    if len(text) > max_len:
        return text[:max_len]
    return text


def useitemgetter():
    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ]
    from operator import itemgetter, attrgetter
    for city in sorted(metro_data, key=itemgetter(1)):
        print(city)
    cc_name = itemgetter(1, 0)
    for city in metro_data:
        print(cc_name(city))

    from mytoolkit import findAllDownloadFile
    cc_path = attrgetter('FullPath')
    paths = [cc_path(f) for f in findAllDownloadFile().values()]
    print(paths)


from abc import ABC, abstractmethod


class LineItem():
    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count


class Order():
    def __init__(self):
        self.cart = []

    def AddItem(self, item):
        self.cart.append(item)


class Promotion(ABC):

    @abstractmethod
    def discount(self, order):
        '''return discount'''


class Buy3Free1Promotion(Promotion):
    '''each 3 item free 1 lowest price item'''

    def discount(self, order):
        items = []
        for item in order.cart:
            for _ in range(item.count):
                items.append((item.price, item.name))
        freeCount = round(len(items)/3.0)
        if freeCount > 0:
            freeitems = sorted(items, key=lambda x: x[0])[:freeCount]
            value = sum([x[0] for x in freeitems])
            print(value)
            return value
        return 0


def calOrder():
    '''策略模式：封装一系列算法，封装起来，可以替换'''
    order = Order()
    item = LineItem('item1', 1, 1)
    order.AddItem(item)
    item = LineItem('item2', 2, 2)
    order.AddItem(item)
    item = LineItem('item1', 1, 3)
    order.AddItem(item)
    item = LineItem('item3', 3, 4)
    order.AddItem(item)
    item = LineItem('item4', 0.5, 2)
    order.AddItem(item)
    item = LineItem('item5', 2, 1)
    order.AddItem(item)
    promotion = Buy3Free1Promotion()
    discount = promotion.discount(order)


def clock(func):
    '''装饰器，计算程序运行时间'''
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        print('装饰器，被装饰的函数定义后立即执行')
        ''''wraps把func属性复制到clocked'''
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time()
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(','.join(repr(a) for a in args))
        if kwargs:
            arg_lst.append(','.join(repr(a) for a in kwargs))
        arg_str = ','.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked


@functools.lru_cache()  # 使用缓存
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-2)+fibonacci(n-1)


@functools.singledispatch
def htmlize(obj):
    '''singledispatch处理object基函数'''
    content = html.escape(repr(obj))
    return '<pre>{}</pre>'.format(content)


@htmlize.register(str)
def _(text):
    '''各个专门函数用'''
    content = html.escape(text).replace('\n', '<br>\n')
    return '<p>{0}</p>'.format(content)


@htmlize.register(numbers.Integral)
def _(n):
    return '<pre>{0} (0x{0:x})</pre>'.format(n)


@htmlize.register(tuple)
def _(seq):
    inner = '<>'


registry = set()


def register(active=True):
    '''参数化的装饰器，第二个才是func'''
    def decorate(func):
        if active:
            registry.add(func)
        else:
            registry.discard(func)
        return func
    return decorate


@register(active=False)
def func1():
    print('running f1()')


@register(active=True)
def func2():
    print('running f2()')


DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'


def clock_withparam(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*args):
            t0 = time.time()
            name = func.__name__
            result = func(*args)
            elapsed = time.time()-t0
            # locals引用clocked的局部变量
            print(fmt.format(**locals()))
            return result
        return clocked
    return decorate


if __name__ == '__main__':
    print(fibonacci(6))
