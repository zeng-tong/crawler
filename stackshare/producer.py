# -*- coding: utf-8 -*-
from stackshare.src.utils import py_redis, toRedisKey, toConsumedKey

from stackshare.src import get_item

redis = py_redis().get_resource()

categories = get_item.get_categories()


# Hash 中存储已经爬取过的id
# list 中存储待爬取的id
def start():
    for category in categories:
        ids = get_item.get_items_ids(category)
        if len(ids) == 0:
            print('Category %s have 0 app id...' % category)
        for _id in ids:
            if not redis.hexists(toConsumedKey(category), _id):
                redis.lpush(toRedisKey(category), _id)

if __name__ == '__main__':
    start()