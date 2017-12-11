# -*- coding: utf-8 -*-
from config import GetLogger
from stackshare.src.constants import CONSUMED, CATEGORY_KEY
from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey

from stackshare.src import get_item

from stackshare.src.utils import mysql_session

from stackshare.src.item_info import itemInfo


redis = PyRedis().get_resource()


class consume:

    def __init__(self):
        self.category = redis.srandmember(CATEGORY_KEY)
    # Hash 中存储已经爬取过的id
    # list 中存储待爬取的id

    def start(self):
        logger = GetLogger('consumer').get_logger()
        # 从 set 获取 待爬取 _id
        ids = self.__get_ids(20)
        while len(ids) != 0:
            items = get_item.get_item(ids, self.category)
            for item in items:
                try:
                    session = mysql_session()
                    session.expunge_all()
                    item_info = itemInfo(app_url=item['url'], name=item['name'])
                    stacks = item_info.get_stacks()
                    session.add(stacks)
                    session.commit()
                    logger.info(msg=item['name'] + ' save to mysql succeed...')
                    # 将 id 加入已爬取 hash. 避免重复爬取
                    redis.hset(name=toConsumedKey(self.category), key=item['id'], value=CONSUMED)
                except Exception as e:
                    logger.warn(e)
                    logger.warn(msg='App 「%s」 under category %s insert error.Please noticing.' % (item['name'], self.category))
                    continue
                finally:
                    session.close()
            ids = self.__get_ids(20)
        # 该category下id消费完, 移出category
        redis.srem(CATEGORY_KEY, self.category)
        logger.info(msg='Process finished...')

    def __get_ids(self, nums):
        ids = []
        for i in range(0, nums):
            _id = redis.spop(toProducerKey(self.category))
            if _id:
                ids.append(_id)
            else:
                return ids
        return ids

if __name__ == '__main__':
    consume().start()
