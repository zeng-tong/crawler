# -*- coding: utf-8 -*-
from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey

from stackshare.src import get_item

redis = PyRedis().get_resource()

categories = get_item.get_categories()


# Hash 中存储已经爬取过的id
# set 中存储待爬取的id
def start():
    for category in categories:
        ids = get_item.get_items_ids(category)
        if len(ids) == 0:
            print('Category %s have 0 app id...' % category)
        for _id in ids:
            if redis.hexists(toConsumedKey(category), _id) or redis.sismember(toProducerKey(category), _id):
                continue
            else:
                redis.sadd(toProducerKey(category), _id)
                print('id %s under category %s put into waiting-to-consume set...' % (_id, category))


if __name__ == '__main__':
    start()
