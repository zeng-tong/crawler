# -*- coding: utf-8 -*-
from config import GetLogger

from stackshare.src.constants import CATEGORY_KEY

from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey, prepareCategories

from stackshare.src import get_item

# Hash 中存储已经爬取过的id
# set 中存储待爬取的id
logger = GetLogger('producer').get_logger()


class produce:
    def start(self):
        category = self.__redis.spop(CATEGORY_KEY)
        while category:
            category = str(category, encoding='utf-8')
            ids = get_item.get_items_ids(category)
            if len(ids) == 0:
                logger.warn(msg='Category %s have 0 app id...' % category)
            for _id in ids:
                if self.__redis.sismember(toConsumedKey(category), _id):
                    continue
                else:
                    self.__redis.lpush(toProducerKey(category), _id)
                    logger.info(msg='id %s under category %s put into waiting-to-consume set...' % (_id, category))
            category = self.__redis.spop(CATEGORY_KEY)

    def __init__(self):
        self.__redis = PyRedis().get_resource()
        prepareCategories()


if __name__ == '__main__':
    produce().start()
