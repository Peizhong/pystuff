# 读取sqlite数据，保存到mysql，用transession,
# 多线程
# 装饰器 不同的表不同的函数，不用关心数据源和目标，装饰后，自动全部执行
# 接口

import time
import functools
from operator import itemgetter
from concurrent import futures

import sqlite3
import pymysql
import pymysql.cursors

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
    # print('加载时立即执行')
    def connect():
        res = func(sqlite=sqlitepath, mysql=mysqlserver)
    jobToRun.append(connect)
    return connect


# key值默认按这个排序
defaultOrder = ['id', 'workspace_id', 'function_location_id', 'asset_id', 'operation_flag', 'update_time',
                'province_code', 'bureau_code', 'power_grid_flag', 'data_from', 'optimistic_lock_version']


@functools.lru_cache()
def getIndex(col: str):
    lowerCol = col.lower()
    if lowerCol in defaultOrder:
        return repr(defaultOrder.index(lowerCol))
    else:
        return 'z'+lowerCol


def insertTable(mysql, tableName, columnInfo, items):
    dropSql = 'drop table if exists %s' % tableName.lower()
    dropSql = 'drop table if exists %s' % tableName.upper()
    keys = sorted(
        (col for col in columnInfo if col[-1] > 0), key=lambda k: k[-1])
    others = sorted(
        (col for col in columnInfo if col[-1] == 0), key=lambda k: getIndex(k[1]))
    basicDef = itemgetter(1, 2)
    justName = itemgetter(1)
    createSql = 'create table `%s` (%s,%s,primary key(%s)) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;' % (
        tableName,
        ','.join(['`%s` %s not null' % basicDef(k) for k in keys]),
        ','.join(['`%s` %s' % basicDef(c) for c in others]),
        ','.join(['`%s`' % justName(k) for k in keys]))
    # print(createSql)

    myconn = pymysql.connect(host=mysql, user='root', password='mypass',
                             db='MYDEV', charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    insertTemplate = 'replace into `%s`(%s) values(%s)' % (tableName, ','.join(
        [justName(c) for c in columnInfo]), ','.join('%s' for c in columnInfo))
    try:
        # ACID:原子性、一致性、隔离性、持久性
        myconn.begin()
        with myconn.cursor() as cursor:
            # create,drop,alter..隐式提交
            cursor.execute(dropSql)
            cursor.execute(createSql)
            #cursor.execute('fuck me')
            # for i in items:
            #cursor.execute(insertTemplate, i)
            print('start write table '+tableName)
            cursor.executemany(insertTemplate, items)
        myconn.commit()
    except Exception as e:
        print(e)
        myconn.rollback()
    finally:
        myconn.close()


@sq2mq
@clock
def copyFunctionLocation(sqlite: 'sqlite 数据库路径', mysql: 'mysql 数据库地址'):
    tableName = 'DM_FUNCTION_LOCATION'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyDevice(sqlite, mysql):
    tableName = 'DM_DEVICE'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyParts(sqlite, mysql):
    tableName = 'DM_PARTS'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyFlAsset(sqlite, mysql):
    tableName = 'DM_FL_ASSET'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyAssetTechparam(sqlite, mysql):
    tableName = 'DM_A_ASSET'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyClassify(sqlite, mysql):
    tableName = 'DM_CLASSIFY'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


@sq2mq
@clock
def copyTechparam(sqlite, mysql):
    tableName = 'DM_TECHPARAM'
    #print('do something from %s to %s' % (sqlite, mysql))
    # with?
    conn = sqlite3.connect(sqlite)
    cur = conn.cursor()
    # create table
    cur.execute('PRAGMA table_info(%s)' % tableName)
    columns = cur.fetchall()
    insertTable(mysql, tableName, columns,
                (r for r in cur.execute('select * from %s' % tableName)))
    # print(cur.fetchone())
    # print(columns)
    cur.close()
    conn.close()
    return 1


MAX_WORKER = 10


def do(func):
    res = func()
    return res


@clock
def doAll():
    workers = min(MAX_WORKER, len(jobToRun))
    # 不同线程中执行
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(do, jobToRun)
    return len(list(res))


@clock
def doOneByOne():
    for job in jobToRun:
        job()


def coroutine(func):
    '装饰器预激协程next'
    @functools.wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer


@coroutine
def coroutineAverager():
    total = 0.0
    count = 0
    average = 0
    while True:
        # yield后面的值发给调用方，然后暂停执行
        # 等调用方把值发个协程，再执行term赋值和后面的代码
        term = yield average
        if term is None:
            # 抛出异常，异常对象保存返回值
            break
        total += term
        count += 1
        average = total/count
        print('coroutineAverager:%r' % average)
    return (average, count)


def doCoroutineAverager():
    from inspect import getgeneratorstate
    coro_avg = coroutineAverager()
    print(getgeneratorstate(coro_avg))
    # send:触发协程
    coro_avg.send(10)
    print(getgeneratorstate(coro_avg))
    coro_avg.send(20)
    try:
        c = coro_avg.send(None)
    except StopIteration as exc:
        result = exc.value
    coro_avg.close()
    print(getgeneratorstate(coro_avg))


if __name__ == '__main__':
    # doOneByOne()
    doAll()
