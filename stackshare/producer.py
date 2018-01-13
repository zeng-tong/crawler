# -*- coding: utf-8 -*-
import asyncio
import re

import aiohttp
from bs4 import BeautifulSoup

from config import GetLogger
from stackshare.src.Utils import constants
from stackshare.src.Utils.constants import  CATEGORIES
from stackshare.src.Utils.utils import PyRedis, toProducerKey, toConsumedKey, loop

# Hash 中存储已经爬取过的id
# set 中存储待爬取的id
logger = GetLogger('producer').get_logger()


class produce:

    def __init__(self):
        self.__redis = PyRedis().get_resource()

    def start(self):
        tasks = []
        for category in CATEGORIES:
            tasks.append(self.fetch(category))
        loop.run_until_complete(asyncio.gather(*tasks))

    async def fetch(self, category):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(constants.DOMAIN + category) as response:
                text = await response.text()
                ids = produce.get_stacks_ids(text)
                for _id in ids:
                    if self.__redis.sismember(toConsumedKey(category), _id):
                        continue
                    else:
                        self.__redis.lpush(toProducerKey(category), _id)
                        logger.info(msg='id %s under category %s put into waiting-to-consume set...' % (_id, category))

    @staticmethod
    def get_stacks_ids(text):
        ids = []
        soup = BeautifulSoup(text, 'lxml')
        try:
            ids = re.search(r'ordered_service_ids = (.*)?]', soup.text, re.M).group(0).replace(
                'ordered_service_ids = ', '')
            ids = eval(ids)
        except Exception as e:
            print(e)
        finally:
            return ids

if __name__ == '__main__':
    produce().start()
