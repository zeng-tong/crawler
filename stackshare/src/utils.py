# -*-coding: utf-8 -*-

from config import PyRedis
from stackshare.src import get_item
from stackshare.src.constants import CATEGORY_KEY

def toProducerKey(category):
    return str(category).replace('/', '')


def toConsumedKey(category):
    return 'consumed_' + toProducerKey(category)


def prepareCategories():
    __redis = PyRedis().get_resource()
    categories = get_item.get_categories()
    for category in categories:
        # category 加入 QUEUE
        __redis.sadd(CATEGORY_KEY, category)
