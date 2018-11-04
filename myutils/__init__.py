import os
import functools
import time
import uuid

from .config import config

def makeDir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 / 符号
    path = path.rstrip("/")
    # 判断路径是否存在
    isExists = os.path.exists(path)
    if not isExists:
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        return False


def query_config(name: str):
    value = config.get(name)
    print('{} is {}'.format(name, value))
    return value


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        arglist = []
        if args:
            arglist.append(', '.join(repr(s) for s in args))
        if kwargs:
            paris = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            arglist.append(','.join(paris))
        elapsed = time.time()-t0
        print('%s(%s): %r' % (func.__name__, arglist, elapsed))
        return res
    return clocked


def new_uuid():
    return uuid.uuid4().hex


def replace_invalid_filename_char(filename, replaced_char='_'):
    '''Replace the invalid characaters in the filename with specified characater.
    The default replaced characater is '_'.
    e.g.
    C/C++ -> C_C++
    '''
    valid_filename = filename
    invalid_characaters = '\\/:*?"<>|'
    for c in invalid_characaters:
        # print 'c:', c
        valid_filename = valid_filename.replace(c, replaced_char)

    return valid_filename

def self_check():
    #directory to ensure
    dirs = query_config('path').values()
    for d in dirs:
        makeDir(d)
    #os info
    from .osinfo import tell_me
    tell_me()
