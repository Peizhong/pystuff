# 读取sqlite数据，保存到mysql，用transession,
# 多线程
# 装饰器 不同的表不同的函数，不用关心数据源和目标，装饰后，自动全部执行
# 接口

import time
import functools

import sqlite3
import pymysql

import mytoolkit


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
    return clocked


jobToRun = []

sqlitepath = mytoolkit.queryConfig('avmtdb')
mysqlserver = mytoolkit.queryConfig('host')


def sq2mq(func):
    'sqlite->mysql'
    print('加载时立即执行')

    def connect():
        res = func(sqlite=sqlitepath, mysql=mysqlserver)

    jobToRun.append(connect)
    return connect


def reorderTable(columnInfo):
    # key值默认按这个排序
    defaultOrder = ['id', 'workspace_id', 'function_location_id', 'asset_id']

    keys = sorted(
        (col for col in columnInfo if col[-1] > 0), key=lambda k: k[-1])
    others = sorted(
        (col for col in columnInfo if col[-1] == 0), key=lambda k: k[1])
    print(list(keys))
    print(list(others))


@sq2mq
@clock
def copyFunctionLocation(sqlite, mysql):
    table_name = 'DM_FUNCTION_LOCATION'
    print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('select * from dm_function_location')
    # print(cur.fetchone())
    cur.execute('PRAGMA table_info(dm_fl_asset)')
    columns = cur.fetchall()
    reorderTable(columns)
    # print(columns)
    cur.close()
    conn.close()


def doAll():
    for job in jobToRun:
        job()


if __name__ == '__main__':
    doAll()
