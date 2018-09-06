import os
import functools
import time
import uuid

from .config import config

def self_check():
    #directory to ensure
    dirs = ('logs','downloads')
    def mkdir(path):
        if not os.path.exists(path):
            os.mkdir(path)
    for d in dirs:
        mkdir(d)
    #os info
    from .osinfo import tell_me
    tell_me()


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
