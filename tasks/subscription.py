import time
from enum import Enum
from collections import namedtuple
from concurrent import futures

import myutils

user_sub = namedtuple('user_sub', 'user_id subscriptions')
sub_detail = namedtuple('sub_detail', 'sub_name sub_link')


class DataSource(Enum):
    Default = 0x0
    MySql = 0x1
    Redis = 0x10
    MySqlRedis = MySql | Redis
    Mock = 0x100


class SubscriptionFactory():
    def __init__(self, source, destination):
        self.maker = None
        self.writer = []
        if source == DataSource.MySql:
            self.maker = get_mysql_subscription
        elif source == DataSource.Redis:
            self.maker = get_redis_subscription
        else:
            self.maker = get_mock_subscription
        if destination == DataSource.Redis:
            self.writer.append(update_redis_subscription)
        elif destination == DataSource.MySql:
            self.writer.append(update_mysql_subscription)
        elif destination == DataSource.MySqlRedis:
            self.writer.append(update_mysql_subscription)
            self.writer.append(update_redis_subscription)

    def get_subscription(self, length=100):
        if not self.maker:
            return None
        return self.maker(length)

    @myutils.clock
    def update_subscription(self, data):
        def dowork(writer):
            print('start: ', writer.__name__)
            writer(data)
            print('done: ', writer.__name__)
        with futures.ThreadPoolExecutor(2) as executor:
            res = executor.map(dowork, self.writer)
        return True


def get_subscription():
    factory = SubscriptionFactory(DataSource.Mock, DataSource.MySqlRedis)
    data = factory.get_subscription()


def update_subscription(data):
    factory = SubscriptionFactory(DataSource.Mock, DataSource.MySql)
    data = factory.update_subscription(data)


def get_article(link):
    pass


def mock():
    factory = SubscriptionFactory(DataSource.Redis, DataSource.Default)
    data = factory.get_subscription(10000)


def get_mock_subscription(count):
    import random
    mock = []
    links = [
        sub_detail('什么值的买', 'www.smzdm.com'),
        sub_detail('爱范儿', 'www.ifanr.com'),
        sub_detail('瘾科技', 'cn.engadget.com'),
        sub_detail('数字尾巴', 'www.dgtle.com')
    ]
    for n in range(1, count):
        linkslen = len(links)
        subs = set(links[random.randint(0, linkslen-1)] for x in range(3))
        mock.append(user_sub(n, list(subs)))
    return mock


def get_redis_subscription(count):
    '''
    sub_user_id: set
    sub_user_[id]_subs_: list:
    '''
    redis = myutils.MyRedis()
    data = redis.get_dict('user_subscription')
    return data


def get_mysql_subscription(count):
    '''将mysql的订阅数据同步到redis
    param mysqlhost: mysql地址
    '''
    result = []
    try:
        with myutils.MyMySQL() as mysql:
            for row in mysql.query('select * from subscriptions_subscription limit %s', count):
                result.append(row)
    except Exception as e:
        print(e)
    return result


def update_mysql_subscription(data):
    with myutils.MyMySQL() as mysql:
        rows = []
        for m in data:
            for s in m.subscriptions:
                r = (m.user_id % 2 + 1, s.sub_name, s.sub_link, '1', 0)
            rows.append(r)
        mysql.replace(
            'replace into `subscriptions_subscription`(user_id,subs_name,subs_link,is_active,count) values(%s,%s,%s,%s,%s)', rows)
    print('write {} subscriptions to mysql'.format(len(rows)))


def update_redis_subscription(data):
    d = dict(data)
    redis = myutils.MyRedis()
    redis.set_dict('user_subscription', d)
    print('write {} subscriptions to redis'.format(len(d)))


def update_subscription_job():
    repo = get_mysql_subscription(1000)
    redis = myutils.MyRedis()
    p = redis.get_pipeline()
    for row in repo:
        p.hset('subscription_job_detail', row['id'], row['subs_link'])
        p.zadd('subscription_job_todo', row['id'], time.time())
    p.execute()


def get_subscription_job(length=1):
    '''从按时间排序的subscription_job_id取出
    '''
    pass


def add_subscription_job(job_ids):
    '''
    key: job_id
    value: 时间戳
    '''
    value = [(job, time.time()) for job in job_ids]
    redis = myutils.MyRedis()
    redis.set_sorted_set('subscription_job', value)
