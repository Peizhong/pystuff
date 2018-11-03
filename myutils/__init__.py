import os
import functools
import time
import uuid

from .config import config

def self_check():
    #directory to ensure
    dirs = ('logs',)
    def mkdir(path):
        if not os.path.exists(path):
            os.makedirs(path)
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
