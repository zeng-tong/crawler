# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup

from config import GetLogger
from stackshare.src.exceptions import InvalidValueException, RequestErrorException

from stackshare.models.stacks import Stacks
from stackshare.src import constants

logger = GetLogger('item_info').get_logger()


class itemInfo:

    __soup = None
    __app_url = ''
    name = ''

    APP_INFO_TYPE_MAP = {
        'fans': '/fans/ajax',
        'votes': '/overview/ajax',
        'stacks': '/in-stacks/ajax',
        'integrations': '/integrations/ajax',
        'star': 'star'
    }

    def get_stacks(self):
        try:
            res = {
                'contents': json.dumps(self.contents()),
                'description': self.description(),
                'star_count': self.count(count_type='star'),
                'votes_count': self.count(count_type='votes'),
                'fans_count': self.count(count_type='fans'),
                'stacks_count': self.count(count_type='stacks'),
                'integrations_count': self.count(count_type='integrations')
            }
            return Stacks(contents=res['contents'], description=res['description'],
                          star_count=res['star_count'], votes_count=res['votes_count'],
                          stacks_count=res['stacks_count'], fans_count=res['fans_count'],
                          integrations_count=res['integrations_count'], name=self.name)
        except Exception as e:
            print(e)
            return None

    def __init__(self, app_url, name=None):
        self.__app_url = app_url
        self.__check_url()
        if name is not None:
            self.name = name
        else:
            self.name = str(app_url).replace('/', '')

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
            raise InvalidValueException('count_type error')
        if count_type == 'star':
            return self.__soup.find('div', 'star-count').get_text()
        else:
            label, cnt = self.__soup.select('a[data-href=%s%s]' % (self.__app_url, self.APP_INFO_TYPE_MAP[count_type]))[0].stripped_strings
            return cnt

    def __check_url(self):
        if self.__app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        logger.debug(msg='Item_info: Start request ' + self.__app_url)
        response = requests.get(constants.DOMAIN + self.__app_url)
        logger.debug(msg='Item_info: Request ' + self.__app_url + ' Succeed...')
        if response.status_code != 200:
            raise RequestErrorException(msg=response.status_code)
        self.__soup = BeautifulSoup(response.text, 'lxml')

if __name__ == '__main__':
    itemInfo(app_url='/python', name='Python')