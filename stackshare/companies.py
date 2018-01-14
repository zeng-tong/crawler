# -*- utf-8 -*-
import asyncio

import aiohttp
import requests

from config import GetLogger, PyRedis
from config import mysql_session
from stackshare.src.Service import CompaniesInfoService, ItemService
from stackshare.src.Utils import constants
from stackshare.src.Utils.constants import CATEGORY_KEY
from stackshare.src.Utils.utils import prepareCategories, loop

logger = GetLogger('companies').get_logger()


class Company:
    def __init__(self):
        self.__redis = PyRedis().get_resource()

    def start(self):
        tasks = []
        category = self.__redis.spop(CATEGORY_KEY)
        while category:
            category = str(category, encoding='utf-8')
            if category == '/trending/new':
                category = self.__redis.spop(CATEGORY_KEY)
                continue
            tasks.append(self.fetch(constants.DOMAIN + category))
            logger.info(msg='Category 「%s」 has putted into crawler' % category)
            category = self.__redis.spop(CATEGORY_KEY)
        pages = loop.run_until_complete(asyncio.gather(*tasks))
        for page in pages:
            self.persist(ItemService.item(page))

    @staticmethod
    async def fetch(url, payload=None, **kwargs):
        async with aiohttp.ClientSession(loop=loop) as session:
            if payload:
                async with session.post(url=url, data=payload) as response:
                    text = await response.text()
                    return text
            else:
                async with session.get(url=url) as response:
                    text = await response.text()
                    return text

    def persist(self, items):
        for item in items:
            result = CompaniesInfoService.CompaniesInfo(item['url']).companies()
            try:
                companies = next(result)
            except Exception as e:
                print('next error , {} now skipped'.format(item['url']))
                logger.error(e)
                continue
            while companies:
                for entity in companies:
                    try:
                        session = mysql_session()
                        session.expunge_all()
                        session.add(entity)
                        session.commit()
                        logger.info(msg='Company 「' + entity.company_name + '」under ' + item['name'] + ' save to mysql succeed...')
                    except Exception as e:
                        print(e)
                        print('Exception when save to MySQL ,plz check...')
                    finally:
                        session.close()
                try:
                    companies = next(result)
                except Exception as e:
                    print('next companies error ,{} now skipped'.format(item['url']))
                    logger.error(e)
if __name__ == '__main__':
    prepareCategories()
    Company().start()



