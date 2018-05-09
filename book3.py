#流畅的python: 介绍python3的特性
import collections

from random import randrange, randint, choice

from math import hypot

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


if __name__ == '__main__':
    desk = FrenchDesk()
    print(desk)
    # choice: 有len,__getitem__
    print(choice(desk))
    for card in sorted(desk, key=spades_high):
        print(card)

l = [1, 3, 5, 7, 9, 11, 13, 15]
# [x,y,z] z:方向/步长，如果为负，从最后开始
l1 = l[:6:-2]
l1 = l[4::-2]

suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)


def spades_high(card):
    rank_value = FrenchDesk.ranks.index(card.rank)
    return rank_value*len(suit_values)+suit_values[card.suit]


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
