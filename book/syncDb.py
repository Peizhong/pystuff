# 读取sqlite数据，保存到mysql，用transession,
# 多线程
# 装饰器 不同的表不同的函数，不用关心数据源和目标，装饰后，自动全部执行
# 接口
import time
import functools
from operator import itemgetter, attrgetter
from abc import ABC, abstractmethod
from concurrent import futures
from time import sleep, strftime

import sqlite3

from mytoolkit import queryConfig, clock

MAX_WORKER = 10

jobToRun = []
sqlitepath = queryConfig('avmtdb')
host = queryConfig('host')


def sq2mq(func):
    'sqlite->mysql'
    # print('加载时立即执行')
    def connect():
        # 传参数进去
        res = func(sqlite=sqlitepath, mysql=host)
        return res
    jobToRun.append(connect)
    return connect


def rd(func):
    '''
    插入redis连接信息
    '''
    @functools.wraps(func)
    def connect(**kwargs):
        kwargs['host'] = host
        res = func(**kwargs)
        return res
    return connect


# column值默认按这个排序
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
    import pymysql
    import pymysql.cursors

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
            # cursor.execute('fuck me')
            # for i in items:
            # cursor.execute(insertTemplate, i)
            print('start write table '+tableName)
            cursor.executemany(insertTemplate, items)
        myconn.commit()
    except Exception as e:
        print(e)
        myconn.rollback()
    finally:
        myconn.close()


class FunctionLocationVO:
    '''
        # 在__dict__中储存实例属性 会消耗内存, 使用__slots__改变属性的存储方式
        # 只能用slot中定义的属性
        # 继承要重写
    __slots__ = ('__id', '__workspaceId', '__flName',
                 '__classifyId', '__parentId')
    '''
    Columns = ('id', 'workspace_id', 'fl_name', 'classify_id', 'fl_type',
               'parent_id', 'fla.asset_id', 'running_state', 'sort_no', 'update_time')

    def __init__(self, id, workspaceId):
        # __标记为私有, 会被改写成_FunctionLocationVO__id, 仍然能访问
        self.__id = id
        self.__workspaceId = workspaceId

    @property
    def Id(self):
        return self.__id

    @property
    def WorkspaceId(self):
        return self.__workspaceId

    @classmethod
    def BuildFromRow(cls, row):
        '''第一个参数是类本身，可用作备选构造方法'''
        ziped = zip(cls.Columns, row)
        packed = {z[0]: z[1] for z in ziped}
        id = packed.get('id')
        workspaceId = packed.get('workspace_id')
        f = FunctionLocationVO(id, workspaceId)
        f.FlName = packed.get('fl_name')
        f.ClassifyId = packed.get('classify_id')
        f.FlType = packed.get('fl_type')
        f.ParentId = packed.get('parent_id')
        f.AssetId = packed.get('fla.asset_id')
        f.SortNo = packed.get('sort_no')
        f.RunningState = packed.get('running_state')
        f.UpdateTime = packed.get('update_time')
        return f

    # 可散列的条件: 支持hash和eq
    def __hash__(self):
        return hash("{}_{}".format(self.__id, self.__workspaceId))

    def __eq__(self, other):
        return self.Id == other.Id and self.WorkspaceId == other.WorkspaceId

    def __str__(self):
        return "{}_{}".format(self.__id, self.__workspaceId)


class AssetObjectVO(ABC):
    def __init__(self):
        pass


# DeviceObject.__mro__
class DeviceObjectVO(AssetObjectVO):
    Columns = ('id', 'device_name', 'classify_id',
               'is_share_device', 'update_time')

    def __init__(self, deviceId):
        AssetObjectVO.__init__(self)
        self.__id = deviceId

    @classmethod
    def BuildFromRow(cls, row):
        d = DeviceObjectVO(row[0])
        d.DeviceName = row[1]
        d.ClassifyId = row[2]
        d.IsShareDeivce = row[3]
        d.UpdateTime = row[4]
        return d

    @property
    def Id(self):
        return self.__id


class PartsObjectVO(AssetObjectVO):
    Columns = ('id', 'parts_name', 'classify_id', 'update_time')

    def __init__(self, partsId):
        AssetObjectVO.__init__(self)
        self.__id = partsId

    @classmethod
    def BuildFromRow(cls, row):
        p = PartsObjectVO(row[0])
        p.PartsName = row[1]
        p.ClassifyId = row[2]
        p.UpdateTime = row[3]
        return p

    @property
    def Id(self):
        return self.__id


class NodeViewModelVO:
    __slots__ = ('__functionlocation', 'ParentNode', 'ChildNodes')

    def __init__(self, functionlocation: FunctionLocationVO):
        self.__functionlocation = functionlocation
        self.ParentNode = None
        self.ChildNodes = None

    @property
    def FunctionLocation(self):
        return self.__functionlocation

    @property
    def Id(self):
        return self.__functionlocation.Id if self.__functionlocation else None

    @property
    def Name(self):
        return self.__functionlocation.FlName if self.__functionlocation else ''

    @property
    def ParentId(self):
        return self.__functionlocation.ParentId if self.__functionlocation else None


def SetFunctionLocationAsset(functions: [], devices: dict, parts: dict):
    for f in functions:
        if f.AssetId:
            if f.FlType == 3:
                f.AssetObject = devices.get(f.AssetId)
            elif f.FlType == 4:
                f.AssetObject = parts.get(f.AssetId)


@functools.lru_cache()
def columnToQuery(classType, header):
    if classType is FunctionLocationVO:
        return ','.join('{}.{}'.format(header, c) if '.' not in c else c for c in FunctionLocationVO.Columns)
    if classType is DeviceObjectVO:
        return ','.join('{}.{}'.format(header, c) if '.' not in c else c for c in DeviceObjectVO.Columns)
    if classType is PartsObjectVO:
        return ','.join('{}.{}'.format(header, c) if '.' not in c else c for c in PartsObjectVO.Columns)
    return header+'.*'


def BuildWorkspaceTree(workspace, functions):
    objectId = workspace[2]
    rootNode = None
    nodeDict = {f.Id: NodeViewModelVO(f) for f in functions}
    for n in nodeDict.values():
        if n.Id == objectId:
            rootNode = n
        parentNode = nodeDict.get(n.ParentId)
        if parentNode:
            n.ParentNode = parentNode
            if not parentNode.ChildNodes:
                parentNode.ChildNodes = []
            parentNode.ChildNodes.append(n)
    return rootNode


def LoadDevice(workspaceId: str)->dict:
    conn = sqlite3.connect(sqlitepath)
    cursor = conn.cursor()
    columns = columnToQuery(DeviceObjectVO, 'd')
    cursor.execute('select {0} from dm_function_location f, dm_fl_asset fla, dm_device d where f.workspace_id = ? and fla.object_type = 5 and f.id = fla.function_location_id and f.workspace_id = fla.workspace_id and fla.asset_id = d.id and fla.workspace_id = d.workspace_id'.format(
        columns), (workspaceId,))
    devices = {d[0]: DeviceObjectVO.BuildFromRow(d) for d in cursor.fetchall()}
    cursor.close()
    conn.close()
    return devices


def LoadParts(workspaceId: str)->dict:
    conn = sqlite3.connect(sqlitepath)
    cursor = conn.cursor()
    columns = columnToQuery(PartsObjectVO, 'p')
    cursor.execute('select {0} from dm_function_location f, dm_fl_asset fla, dm_parts p where f.workspace_id = ? and fla.object_type = 6 and f.id = fla.function_location_id and f.workspace_id = fla.workspace_id and fla.asset_id = p.id and fla.workspace_id = p.workspace_id'.format(
        columns), (workspaceId,))
    parts = {p[0]: PartsObjectVO.BuildFromRow(p) for p in cursor.fetchall()}
    cursor.close()
    conn.close()
    return parts


def LoadFunctionLocation(workspaceId: str):
    conn = sqlite3.connect(sqlitepath)
    cursor = conn.cursor()
    columns = columnToQuery(FunctionLocationVO, 'f')
    cursor.execute('select {0} from dm_function_location f left join dm_fl_asset fla on f.id = fla.function_location_id where f.workspace_id = ?'.format(
        columns,), (workspaceId,))
    functionlocations = tuple(FunctionLocationVO.BuildFromRow(f)
                              for f in cursor.fetchall())
    cursor.close()
    conn.close()
    devices = LoadDevice(workspaceId)
    parts = LoadParts(workspaceId)
    SetFunctionLocationAsset(functionlocations, devices, parts)
    del devices
    del parts
    return functionlocations


@clock
def LoadMainTransBill(businessCode):
    # 查询对应工作区数据
    conn = sqlite3.connect(sqlitepath)
    cursor = conn.cursor()
    #cursor.execute('select w.id,workspace_name,w.object_id from dm_workspace w, dm_main_transfer m where m.BUSINESS_BILL_CODE = ? and m.id = w.BUSINESS_BILL_ID', (businessCode,))
    cursor.execute(
        'select w.id,workspace_name,w.object_id from dm_workspace w')
    workspaces = cursor.fetchall()
    workspaceFunctions = tuple(LoadFunctionLocation(w[0]) for w in workspaces)

    cursor.close()
    conn.close()
    cursor = None
    conn = None
    workspaceNodes = []
    for param in zip(workspaces, workspaceFunctions):
        future = BuildWorkspaceTree(param[0], param[1])
        workspaceNodes.append(future)
    '''
    cpython阻塞型io用线程才有用
    with futures.ThreadPoolExecutor(2) as executor:
        jobs = []
        for param in zip(workspaces, workspaceFunctions):
            future = executor.submit(BuildWorkspaceTree, param[0], param[1])
            jobs.append(future)
        for future in futures.as_completed(jobs):
            workspaceNodes.append(future.result())
    '''
    total = sum(len(f) for f in workspaceFunctions)
    print('query {} funcionts in {} workspaces'.format(total, len(workspaces)))
    return workspaceNodes


@sq2mq
@clock
def copyFunctionLocation(sqlite: 'sqlite 数据库路径', mysql: 'mysql 数据库地址'):
    tableName = 'DM_FUNCTION_LOCATION'
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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
    # print('do something from %s to %s' % (sqlite, mysql))
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


def do(func):
    res = func()
    return res


@clock
def doAll():
    workers = min(MAX_WORKER, len(jobToRun))
    # 不同线程中执行
    with futures.ThreadPoolExecutor(workers) as executor:
        # 线程池运行可调用对象
        # 受GIL全局解释器锁的限制，并不是并行，但对I/O密集型的无影响
        # Python的实现方式: CPyton, Pypy, IronPython
        # CPython, 将Python源码编译成CPython字节码，然后再由虚拟机运行
        # CPython兼容c编写的扩展
        # PyPy使用JIT，动态编译，性能提升，但第三方模块兼容不好
        # I/O操作，等待系统返回时，或者time.sleep()，会释放GIL
        # 返回一个生成器，返回结果与调用顺序一致
        res = executor.map(do, jobToRun)
        print('result is out')
    print('result is really out')
    return len(list(res))


def arcfour_test(size):
    print('do {} '.format(size))
    for i in range(1, size):
        for j in range(1, size):
            for k in range(1, size):
                v = (i+j*k)/k*(43/j+i*k)
    sleep(size/10)
    return v


@clock
def doAllCpu():
    # 有4个进程的话会启动4次..
    with futures.ProcessPoolExecutor() as executor:
        to_do = []
        for j in range(10, 30):
            # 期物
            future = executor.submit(arcfour_test, j)
            to_do.append(future)
        result = []
        # 等待运行完毕
        for future in futures.as_completed(to_do):
            res = future.result()
            result.append(res)
    return len(result)


@clock
def doAllWithDetail():
    workers = min(MAX_WORKER, len(jobToRun))
    with futures.ThreadPoolExecutor(max_workers=workers) as executor:
        to_do = []
        for j in jobToRun:
            # 排定可调用对象的执行时间，返回一个期物
            future = executor.submit(do, j)
            to_do.append(future)
            print('Scheduled for {}:{}'.format(j.__name__, future))
        result = []
        for future in futures.as_completed(to_do):
            # 完成后返回结果
            res = future.result()
            print('{}:{}'.format(future, res))
            result.append(res)
    return len(result)


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


@rd
def redisTest(**kwargs):
    import redis
    # 连接池？
    r = redis.Redis(host=kwargs['host'], port=6379)
    r.set('hello', 'aad你好吗')
    v = r.get('hello')
    str_utf8 = v.decode('utf-8')
    print(str_utf8)

    # redis key和5种数据类型的映射：string(字符串、整数、浮点)、list链表、set集合、hash散列表(键值对)、zset有序集合
    # 附加功能：发布/订阅，主从复制、持久化
    # 字符串
    r.set('counter', 1)
    # 计数器
    r.incr('counter')
    r.incr('counter')
    print(r.get('counter'))
    r.decr('counter')
    print(r.get('counter'))
    # list
    r.rpush('rlist', 'mimi')
    r.rpush('rlist', 'jj')
    r.lrange('rlist', 0, -1)
    r.lindex('rlist', 1)
    # set
    r.sadd('rset', '1234')
    r.sadd('rset', '01234')
    r.srem('rset', '123')
    r.sadd('rset', 'mii')
    r.smembers('rset')
    r.sismember('rset', '1234')
    # hash
    r.hset('rhash', 1, '3234')
    r.hset('rhash', 2, '3234')
    r.hgetall('rhash')
    r.hget('rhash', 1)
    r.hdel('rhash', 2)


if __name__ == '__main__':
    redisTest()
