# -*- utf-8 -*-
import requests
from config import GetLogger, PyRedis
from stackshare.src import get_item, constants, companies_info
from config import mysql_session
from stackshare.src.constants import CATEGORY_KEY
from stackshare.src.utils import prepareCategories

logger = GetLogger('companies').get_logger()


class Company:
    def __init__(self):
        self.__redis = PyRedis().get_resource()

    def start(self):
        category = self.__redis.spop(CATEGORY_KEY)
        while category:
            category = str(category, encoding='utf-8')
            if category == '/trending/new':
                category = self.__redis.spop(CATEGORY_KEY)
                continue
            self.save(category)
            category = self.__redis.spop(CATEGORY_KEY)
        logger.info(msg='Process finished')

    def save(self, category):
        items = get_item.get_item(requests.get(constants.DOMAIN + category))
        for item in items:
            result = companies_info.CompaniesInfo(item['url']).companies()
            companies = next(result)
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
                    finally:
                        session.close()
                companies = next(result)


if __name__ == '__main__':
    prepareCategories()
    Company().start()



