# 迭代器:从集合中去数据，生成器凭空生成数据
# 迭代器模式: 防止内存等、一次获取一个数据，yield关键字构建生成器generator
# 标准迭代器有2个方法: __next__, __iter__
from collections import abc
import re
RE_WORD = re.compile('\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self):
        return 'Sentence(%s)' % self.text

    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            yield match.group()
        return
        '''实现了__getitem__(self,index)也能迭代'''
        for word in self.words:
            yield word
        return


v = Sentence('abc')
b = isinstance(v, abc.Iterable)

# 生成器当作协程
# __next()__只允许从生成器中获得数据
# .send()允许生成器的调用方将数据编程yield的值
