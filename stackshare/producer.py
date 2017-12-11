# -*- coding: utf-8 -*-
from config import GetLogger
from stackshare.src.constants import CATEGORY_KEY
from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey

from stackshare.src import get_item

redis = PyRedis().get_resource()

class produce:
# Hash 中存储已经爬取过的id
# set 中存储待爬取的id
    def start(self):
        logger = GetLogger('producer').get_logger()

        categories = get_item.get_categories()

        for category in categories:
            # category 加入 QUEUE
            redis.sadd(CATEGORY_KEY, category)
            ids = get_item.get_items_ids(category)
            if len(ids) == 0:
                logger.warn(msg='Category %s have 0 app id...' % category)
            for _id in ids:
                if redis.hexists(toConsumedKey(category), _id):
                    continue
                else:
                    redis.sadd(toProducerKey(category), _id)
                    logger.info(msg='id %s under category %s put into waiting-to-consume set...' % (_id, category))


if __name__ == '__main__':
    produce().start()
