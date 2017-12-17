# -*- coding: utf-8 -*-
import requests

from config import GetLogger
from stackshare.src.constants import CATEGORY_KEY, DOMAIN
from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey

from stackshare.src import get_item

from config import mysql_session

from stackshare.src.item_info import itemInfo


redis = PyRedis().get_resource()
logger = GetLogger('consumer').get_logger()


class consume:
    def __init__(self):
        self.category = str(redis.srandmember(CATEGORY_KEY), encoding="utf-8")
    # Hash 中存储已经爬取过的id
    # list 中存储待爬取的id

    def start(self):
        # 最热10条
        self.__get_hottest()
        # 从 set 获取 待爬取 _id
        ids = self.__get_ids(9)
        while len(ids) != 0:
            items = get_item.get_items(ids, self.category)
            for item in items:
                try:
                    session = mysql_session()
                    session.expunge_all()
                    item_info = itemInfo(app_url=item['url'], name=item['name'])
                    stacks = item_info.get_stacks()
                    session.add(stacks)
                    session.commit()
                    logger.info(msg=item['name'] + ' save to mysql succeed...')
                except Exception as e:
                    logger.warn(e)
                    logger.warn(msg='App 「%s」 under category %s insert error.Please noticing.' % (item['name'], self.category))
                    continue
                finally:
                    session.close()
            ids = self.__get_ids(9)
            # 将 id 加入已爬取 hash. 避免重复爬取
            redis.sadd(toConsumedKey(category=self.category), ids)
        # 该category下id消费完, 移出category
        redis.srem(CATEGORY_KEY, self.category)
        logger.info(msg='Process finished...')

    def __get_ids(self, nums):
        ids = []
        for i in range(0, nums):
            _id = redis.rpop(toProducerKey(self.category))
            if _id:
                ids.append(int(_id))
            else:
                return ids
        return ids

    def __get_hottest(self):
        response = requests.get(DOMAIN + self.category)
        items = get_item.get_item(response)
        for item in items:
            try:
                session = mysql_session()
                session.expunge_all()
                item_info = itemInfo(app_url=item['url'], name=item['name'])
                stacks = item_info.get_stacks()
                session.add(stacks)
                session.commit()
                logger.info(msg=item['name'] + ' save to mysql succeed...')
            except Exception as e:
                logger.warn(e)
                logger.warn(msg='App 「%s」 under category %s insert error.Please noticing.' % (item['name'], self.category))
                continue
            finally:
                session.close()


if __name__ == '__main__':
    consume().start()
