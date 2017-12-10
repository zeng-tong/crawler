# -*- coding: utf-8 -*-
from stackshare.src.constants import CONSUMED
from stackshare.src.utils import py_redis, toRedisKey, toConsumedKey

from stackshare.src import get_item

from stackshare.src.utils import mysql_session

from stackshare.src.item_info import itemInfo


redis = py_redis().get_resource()

categories = get_item.get_categories()


# Hash 中存储已经爬取过的id
# list 中存储待爬取的id
def start(category):
        _id = redis.lpop(category)
        while _id:
            item = get_item.get_item(list(_id), category)
            try:
                session = mysql_session()
                item_info = itemInfo(app_url=item['url'], name=item['name'])
                stacks = item_info.get_stacks()
                session.add(stacks)
                session.commit()
                session.close()
                print(stacks.name + ' succed...')
                redis.hset(toConsumedKey(category), _id, CONSUMED)
            except Exception as e:
                redis.lpush(toRedisKey(category), _id)
                print(e)
        print('Process finished...')