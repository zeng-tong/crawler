# -*-coding: utf-8 -*-
import redis

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from stackshare.exceptions import RequestErrorException

engine = create_engine('mysql+pymysql://root:123456@138.197.95.94/stackshare?charset=utf8')


def mysql_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()


class py_redis:

    def __init__(self):
        self.redis_pool = redis.ConnectionPool(host='138.197.95.94', port=6379)

    def get_resource(self):
        try:
            return redis.Redis(connection_pool=self.redis_pool)
        except Exception as e:
            raise RequestErrorException(msg=str(e))
