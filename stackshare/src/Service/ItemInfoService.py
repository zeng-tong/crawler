# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup

from config import GetLogger
from stackshare.src.Utils.constants import DOMAIN
from stackshare.src.Utils.exceptions import InvalidValueException
from stackshare.src.models.stacks import Stacks

logger = GetLogger('item_info').get_logger()


class itemInfo:

    __soup = None

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
                'name': self.name(),
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
                          integrations_count=res['integrations_count'], name=res['name'])
        except Exception as e:
            print(e)
            return None

    def __init__(self, text):
        self.__soup = BeautifulSoup(text, 'lxml')
        self.stack_token = self.__soup.find('meta', property='og:url')['content'].replace(DOMAIN, '')

    def name(self):
        return self.__soup.find('div', id='service-name').find('a', itemprop='name').get_text()

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
            label, cnt = self.__soup.select('a[data-href=%s%s]' % (self.stack_token, self.APP_INFO_TYPE_MAP[count_type]))[0].stripped_strings
            return cnt

if __name__ == '__main__':
    resp = requests.get(DOMAIN + '/bootstrap')
    itemInfo(resp.text).get_stacks()