# -*- utf-8 -*-
import requests
from config import GetLogger
from stackshare.src import get_item, constants, companies_info
from config import mysql_session

logger = GetLogger('companies').get_logger()


def start():
    categories = get_item.get_categories()
    for each in categories:
        if each == '/trending/new':
            continue
        items = get_item.get_item(requests.get(constants.DOMAIN + each))
        for item in items:
            result = companies_info.companies_info(item['url']).companies()
            companies = next(result)
            while companies:
                for entity in companies:
                    try:
                        session = mysql_session()
                        session.expunge_all()
                        session.add(entity)
                        session.commit()
                        logger.info(msg='Company 「' + entity.company_name + '」 save to mysql succeed...')
                    except Exception as e:
                        print(e)
                    finally:
                        session.close()
                companies = next(result)
    logger.info(msg='Process finished')

if __name__ == '__main__':
    start()



