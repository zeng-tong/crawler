# -*-coding: utf-8 -*-
from sqlalchemy import create_engine

import redis
from sqlalchemy.orm import sessionmaker

from stackshare.src.exceptions import RequestErrorException


def mysql_session():
    engine = create_engine('mysql+pymysql://root:123456@138.197.95.94/stackshare?charset=utf8')
    DBSession = sessionmaker(bind=engine)
    return DBSession()


redis_pool = redis.ConnectionPool(host='138.197.95.94', port=6379)


class PyRedis:
    def __init__(self):
        self.__redis_pool = redis_pool

    def get_resource(self):
        try:
            return redis.Redis(connection_pool=self.__redis_pool)
        except Exception as e:
            raise RequestErrorException(msg=str(e))

    def __repr__(self):
        return str(self.__dict__)


def toProducerKey(category):
    return str(category).replace('/', '')


def toConsumedKey(category):
    return 'consumed_' + toProducerKey(category)
