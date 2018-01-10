# -*-coding: utf-8 -*-

from config import PyRedis
from stackshare.src.Service import ItemService
from stackshare.src.Utils.constants import CATEGORY_KEY

def toProducerKey(category):
    return str(category).replace('/', '')


def toConsumedKey(category):
    return 'consumed_' + toProducerKey(category)


def prepareCategories():
    __redis = PyRedis().get_resource()
    categories = ItemService.get_categories()
    for category in categories:
        # category 加入 QUEUE
        if category != '/trending/new':
            __redis.sadd(CATEGORY_KEY, category)
