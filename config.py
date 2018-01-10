# -*- coding: utf-8 -*-
import datetime
import logging
import logging.handlers
import sys

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stackshare.src.Utils.exceptions import RequestErrorException


class GetLogger:

    def __init__(self, name):
        self.name = name
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='[%Y-%m-%d %H:%M:%S]',
                            stream=sys.stdout)

    def get_logger(self):
        file_handler = logging.FileHandler(filename='stackshare/log/%s_%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d'), self.name), mode='a+', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger = logging.getLogger(self.name)
        logger.addHandler(file_handler)
        return logger


def mysql_session():
    engine = create_engine('mysql+pymysql://root@127.0.0.1/stackshare?charset=utf8')
    DBSession = sessionmaker(bind=engine)
    return DBSession()


redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)


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


