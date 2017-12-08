# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from stackshare import constants
from stackshare.exceptions import InvalidValueException


class ItemInfo:
    # 获取app的目录
    @classmethod
    def contents(cls, app_url=None):
        if app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        response = requests.get(constants.DOMAIN + app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            contents = []
            for content in soup.find_all('li', itemprop='itemListElement'):
                if content.find('span', itemprop='name').get_text():
                    contents.append(content.find('span', itemprop='name').get_text())
            return contents
        else:
            return None

    # 获取描述
    @classmethod
    def description(cls, app_url=None):
        if app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        response = requests.get(constants.DOMAIN + app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup.find('span', itemprop='alternativeHeadline').get_text()
        else:
            return None

    # 获取 star 数量
    @classmethod
    def start_count(cls, app_url=None):
        if app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        response = requests.get(constants.DOMAIN + app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup.find('div', 'star-count').get_text()
        else:
            return None

    # TODO
    # 获取 Votes 数量
    @classmethod
    def votes(cls, app_url=None):
        response = cls.__chk_app_url(app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            print(soup.select('a[data-href=%s/overview/ajax]' % app_url))

        else:
            return None

    @staticmethod
    def __chk_app_url(app_url):
        if app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        return requests.get(constants.DOMAIN + app_url)





