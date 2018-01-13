# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from bs4 import BeautifulSoup

from config import GetLogger
from config import mysql_session
from stackshare.src.Service.ItemInfoService import itemInfo
from stackshare.src.Utils import constants
from stackshare.src.Utils.constants import CATEGORIES
from stackshare.src.Utils.utils import PyRedis, toProducerKey, toConsumedKey, loop

redis = PyRedis().get_resource()
logger = GetLogger('consumer').get_logger()


class consume:

    @staticmethod
    async def fetch(url, payload=None, **kwargs):
        callback = kwargs.pop('callback', None)
        async with aiohttp.ClientSession(loop=loop) as session:
            if payload:
                async with session.post(url, data=payload) as response:
                    text = await response.text()
                    if callback:
                        callback(text, kwargs.pop('category', ''))
                    else:
                        return text
            else:
                async with session.get(url) as response:
                    text = await response.text()
                    if callback:
                        callback(text, kwargs.pop('category', ''))
                    else:
                        return text

    def start(self):
        # 最热10条
        self.__get_hottest()
        for category in CATEGORIES:
            self.get_items(category, 10)
            logger.info(msg='Category 「%s」 Process finished...' % category)

    def get_items(self, category, offset):
        isEmpty = False
        tasks = []
        while True:
            if isEmpty:
                break
            payload = {'ids[]': []}
            for i in range(0, offset):
                _id = redis.rpop(toProducerKey(category))
                if _id:
                    payload['ids[]'].append(int(_id))
                else:
                    isEmpty = True
                    break
            redis.sadd(toConsumedKey(category=category), payload['ids[]'])
            tasks.append(self.fetch(url=constants.DOMAIN + category + '/load-more',
                                    payload=payload))
        items = loop.run_until_complete(asyncio.gather(*tasks))
        for item in items:
            self.get_items_response(item, category)

    def __get_hottest(self):
        tasks = []
        loop = asyncio.get_event_loop()
        for category in CATEGORIES:
            tasks.append(self.fetch(url=constants.DOMAIN + category))
        texts = loop.run_until_complete(asyncio.gather(*tasks))
        for text in texts:
            self.get_items_response(text, 'HOTTEST')

    @staticmethod
    def get_items_response(text, category):
        loop = asyncio.get_event_loop()
        soup = BeautifulSoup(text, 'lxml')
        tasks = []
        for data in soup.find_all('div', 'thumbnail-home'):
            try:
                stack_url = data.find('a')['href']
                if stack_url:
                    tasks.append(consume.fetch(url=constants.DOMAIN + stack_url))
            except Exception as e:
                logger.warn(e)
        stack_texts = loop.run_until_complete(asyncio.gather(*tasks))
        for stack in stack_texts:
            consume.persist(stack, category)

    @staticmethod
    def persist(item, category):
        global stacks
        try:
            stacks = itemInfo(item).get_stacks()
            session = mysql_session()
            session.expunge_all()
            session.add(stacks)
            session.commit()
            logger.info(msg='App 「%s」under category %s save to mysql succeed...' % (stacks.name, category))
        except Exception as e:
            logger.error(e)
            logger.error(msg='App 「%s」 under category %s insert error.Please noticing.' % (stacks.name, category))
        finally:
            session.close()


if __name__ == '__main__':
    consume().start()
