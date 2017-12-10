# -*-coding: utf-8 -*-
from sqlalchemy import create_engine

import redis
from sqlalchemy.orm import sessionmaker

from stackshare.src.exceptions import RequestErrorException

engine = create_engine('mysql+pymysql://root:123456@138.197.95.94/stackshare?charset=utf8')

def mysql_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()

redis_pool = redis.ConnectionPool(host='138.197.95.94', port=6379)


class py_redis:

    def __init__(self):
        self.__redis_pool = redis_pool

    def get_resource(self):
        try:
            return redis.Redis(connection_pool=self.__redis_pool)
        except Exception as e:
            raise RequestErrorException(msg=str(e))


def toRedisKey(category):
    return str(category).replace('/', '')


def toConsumedKey(category):
    return 'consumed_' + toRedisKey(category)

if __name__ == '__main__':
    pyredis = py_redis()
    redis = pyredis.get_resource()
    redis.lpush('test', 'test xxxx')
    print(redis.lpop('test'))
