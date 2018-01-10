# -*- coding: utf-8 -*-
import requests

from config import GetLogger
from config import mysql_session
from stackshare.src.Service import ItemService
from stackshare.src.Service.ItemInfoService import itemInfo
from stackshare.src.Utils.constants import CATEGORY_KEY, DOMAIN
from stackshare.src.Utils.utils import PyRedis, toProducerKey, toConsumedKey

redis = PyRedis().get_resource()
logger = GetLogger('consumer').get_logger()


class consume:
    def __init__(self):
        self.category = str(redis.srandmember(CATEGORY_KEY), encoding="utf-8")

    def start(self):
        # 最热10条
        self.__get_hottest()
        # 从 set 获取 待爬取 _id
        ids = self.__get_ids(count=9)
        while len(ids):
            items = ItemService.get_items(ids, self.category)
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
                    logger.error(e)
                    logger.error(msg='App 「%s」 under category %s insert error.Please noticing.' % (item['name'], self.category))
                    continue
                finally:
                    session.close()
            redis.sadd(toConsumedKey(category=self.category), ids)
            ids = self.__get_ids(count=9)
        # 该category下id消费完, 移出.
        redis.srem(CATEGORY_KEY, self.category)
        logger.info(msg='Category 「%s」 Process finished...' % self.category)

    def __get_ids(self, count):
        ids = []
        for i in range(0, count):
            _id = redis.rpop(toProducerKey(self.category))
            if _id:
                ids.append(int(_id))
            else:
                return ids
        return ids

    def __get_hottest(self):
        response = requests.get(DOMAIN + self.category)
        items = ItemService.item(response)
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
                logger.error(e)
                logger.error(msg='App 「%s」 under category %s insert error.Please noticing.' % (item['name'], self.category))
                continue
            finally:
                session.close()


if __name__ == '__main__':
    consume().start()
