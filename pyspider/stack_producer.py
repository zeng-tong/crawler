# -*- encoding: utf-8 -*-
# Created on 2017-12-15 14:42:40
# Project: stackshare_producer

import re
import redis
from pyspider.libs.base_handler import *
from bs4 import BeautifulSoup

URL = 'https://stackshare.io'
redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)


def consumedKey(category):
    return 'consumed' + category


def redis_resource():
    try:
        return redis.Redis(connection_pool=redis_pool)
    except Exception as e:
        print(e)
        raise Exception('Error on get resource from redis pool')


class Handler(BaseHandler):
    crawl_config = {
    }

    def on_start(self):
        self.crawl('https://stackshare.io/categories', callback=self.index_page)

    def index_page(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        div = soup.find('li', 'hide-4').find('div', 'navmenu')
        for each in div.find_all('a'):
            self.crawl(URL + each['href'], save={'category': str(each['href']).replace('/', '')},
                       callback=self.get_items_ids)

    def get_items_ids(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        ids = None
        try:
            ids = re.search(r'ordered_service_ids = (.*)?]', soup.text, re.M).group(0).replace('ordered_service_ids = ',
                                                                                               '')
            ids = eval(ids)
        except Exception as e:
            print(e)
            print(response.url + ' cannot get app\'s ids, and had skipped.')
            return ids
        redis = redis_resource()
        for _id in ids:
            if redis.sismember(consumedKey(response.save['category']), _id):
                print('id: %s under %s had already crawlered, auto skip done' % (_id, response.save['category']))
                continue
            else:
                redis.lpush(response.save['category'], _id)
        return {response.save['category']: ids}
