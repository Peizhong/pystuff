from .config import query_config

from abc import ABC, abstractmethod

import json

import pymysql
import pymysql.cursors

import redis


class AbsSQL(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc, value, traceback):
        pass

    @abstractmethod
    def query(self, sql, *params):
        pass

    @abstractmethod
    def replace(self, sql, items):
        pass


class MyMySQL(AbsSQL):
    host = query_config('host')

    def __init__(self):
        pass

    def __enter__(self):
        self.conn = pymysql.connect(host=MyMySQL.host, user='root', password='mypass',
                                    db='MYDEV', charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        return self

    def __exit__(self, exc, value, traceback):
        print('close mysql')
        self.conn.close()

    def query(self, sql, *params):
        result = []
        with self.conn.cursor() as cursor:
            cursor.execute(sql, *params)
            for row in cursor.fetchall():
                result.append(row)
        return result

    def replace(self, sql, items):
        try:
            # ACID:原子性、一致性、隔离性、持久性
            self.conn.begin()
            with self.conn.cursor() as cursor:
                count = cursor.executemany(sql, items)
            self.conn.commit()
        except Exception as e:
            print(e)
            self.conn.rollback()
        return count


class AbsMemCache(ABC):
    @abstractmethod
    def set_dict(self, name, items):
        pass

    @abstractmethod
    def get_dict(self, name):
        pass

    def bytetostring(self, byts):
        return str(byts, encoding='utf-8')


class MyRedis(AbsMemCache):
    host = query_config('host')
    pool = redis.ConnectionPool(host=host, port=6379)

    def __init__(self):
        self.conn = redis.Redis(connection_pool=MyRedis.pool)

    def get_pipeline(self):
        p = self.conn.pipeline()
        return p

    def set_dict(self, name, items):
        self.conn.delete(name)
        p = self.conn.pipeline()
        for key, value in items.items():
            p.hset(name, repr(key), json.dumps(value))
        p.execute()

    def get_dict(self, name):
        values = {}
        data = self.conn.hgetall(name)
        for k, v in data.items():
            values[k.decode()] = v.decode()
        return values

    def set_sorted_set(self, name, items):
        p = self.conn.pipeline()
        for i in items:
            p.zadd(name, i[0], i[1])
        p.execute()
