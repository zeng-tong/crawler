# -*- encoding: utf-8 -*-
# Created on 2017-12-15 14:43:11
# Project: stackshare_consumer

import requests
import json
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
            if each['href'] == '/trending/new':
                continue
            # self.crawl(URL + each['href'], callback=self.get_item, priority=1)
            self.crawl(URL + each['href'], save={'category': str(each['href']).replace('/', '')},
                       callback=self.get_items_ids, priority=2)

    def get_items_ids(self, response):

        self.get_item(response)

        redis = redis_resource()
        _id = redis.rpop(response.save['category'])
        while _id:
            _id = int(_id)
            payload = {'ids[]': _id}

            req = requests.post(response.url + '/load-more', data=payload)
            self.get_item(req)
            # self.crawl(response.url + '/load-more', data=payload, method='POST', callback=self.get_item)
            redis.sadd(consumedKey(response.save['category']), _id)
            _id = redis.rpop(response.save['category'])

    def get_item(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        for data in soup.find_all('div', 'thumbnail-home'):
            name = data.find('span', itemprop='keywords').get_text()
            app_url = data.find('a')['href']
            self.crawl(URL + app_url, save={'name': name, 'app_url': app_url}, callback=self.get_info)

    def get_info(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        stacks = itemInfo(name=response.save['name'], soup=soup, app_url=response.save['app_url']).get_stacks()
        return stacks


class itemInfo:
    APP_INFO_TYPE_MAP = {
        'fans': '/fans/ajax',
        'votes': '/overview/ajax',
        'stacks': '/in-stacks/ajax',
        'integrations': '/integrations/ajax',
        'star': 'star'
    }

    def __init__(self, name=None, soup=None, app_url=None):
        self.name = name
        self.__soup = soup
        self.__app_url = app_url

    def get_stacks(self):
        try:
            return {
                'name': self.name,
                'contents': json.dumps(self.contents()),
                'description': self.description(),
                'star_count': self.count(count_type='star'),
                'votes_count': self.count(count_type='votes'),
                'fans_count': self.count(count_type='fans'),
                'stacks_count': self.count(count_type='stacks'),
                'integrations_count': self.count(count_type='integrations')
            }
        except Exception as e:
            print(e)
            return None

    # 获取app的目录
    def contents(self):
        contents = []
        for content in self.__soup.find_all('li', itemprop='itemListElement'):
            if content.find('span', itemprop='name').get_text():
                contents.append(content.find('span', itemprop='name').get_text())
        return contents

    # 获取描述
    def description(self):
        return self.__soup.find('span', itemprop='alternativeHeadline').get_text()

    # 获取 Stars, Votes, Fans, Stacks, Integrations 数量
    def count(self, count_type=None):
        if count_type not in self.APP_INFO_TYPE_MAP:
            raise Exception('count_type error')
        if count_type == 'star':
            return self.__soup.find('div', 'star-count').get_text()
        else:
            label, cnt = self.__soup.select('a[data-href=%s%s]' % (self.__app_url, self.APP_INFO_TYPE_MAP[count_type]))[
                0].stripped_strings
            return cnt
