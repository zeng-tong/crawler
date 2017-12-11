# -*- coding: utf-8 -*-
from config import GetLogger
from stackshare.src.constants import CONSUMED
from stackshare.src.utils import PyRedis, toProducerKey, toConsumedKey

from stackshare.src import get_item

from stackshare.src.utils import mysql_session

from stackshare.src.item_info import itemInfo


redis = PyRedis().get_resource()


# Hash 中存储已经爬取过的id
# list 中存储待爬取的id
def start(category):
        logger = GetLogger('consumer').get_logger()
        # 从 set 获取 待爬取 _id
        _id = redis.spop(toProducerKey(category))
        while _id:
            _id = int(_id)
            if redis.hexists(toConsumedKey(category), _id):
                logger.warn(msg='id %s under category %s had already exist in consumed hash, now skipped...' % (_id, category))
                continue
            items = get_item.get_item([_id], category)
            for item in items:
                try:
                    session = mysql_session()
                    session.expunge_all()
                    item_info = itemInfo(app_url=item['url'], name=item['name'])
                    stacks = item_info.get_stacks()
                    session.add(stacks)
                    session.commit()
                    logger.info(msg=item['name'] + ' save to mysql succeed...')
                    # 将 _id 加入已爬取 hash. 避免重复爬取
                    redis.hset(name=toConsumedKey(category), key=_id, value=CONSUMED)
                except Exception as e:
                    logger.warn(e)
                    logger.warn(msg='id %s under category %s insert error.Please noticing.' % (_id, category))
                    continue
                finally:
                    session.close()
            _id = redis.spop(toProducerKey(category))
        logger.info(msg='Process finished...')


if __name__ == '__main__':
    start('/application_and_data')
