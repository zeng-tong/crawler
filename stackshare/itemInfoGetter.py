# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
from stackshare.models.stacks import Stacks
from stackshare import constants
from stackshare.exceptions import InvalidValueException


class ItemInfo:

    __app_url = ''
    response = None

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
                          stacks_count=res['stacks_count'],fans_count=res['fans_count'],
                          integrations_count=res['integrations_count'])
        except Exception as e:
            print(e)
            return None

    def __init__(self, app_url):
        self.__app_url = app_url

    # 获取app的目录
    def contents(self):
        response = self.__check_url(self.__app_url)
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
    def description(self):
        response = self.__check_url(self.__app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup.find('span', itemprop='alternativeHeadline').get_text()
        else:
            return None

    # 获取 Stars, Votes, Fans, Stacks, Integrations 数量
    def count(self, count_type=None):
        if count_type not in self.APP_INFO_TYPE_MAP:
            raise InvalidValueException('count_type error')
        response = self.__check_url(self.__app_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            if count_type == 'star':
                return soup.find('div', 'star-count').get_text()
            else:
                label, cnt = soup.select('a[data-href=%s%s]' % (self.__app_url, self.APP_INFO_TYPE_MAP[count_type]))[
                    0].stripped_strings
            return cnt
        else:
            return None

    # 获取 公司名称
    def companies(self):
        headers = {'Cookie': 'ajs_anonymous_id=%22a1aad3a2-0df8-41f8-9ca0-b61008d9f68d%22; __uvt=; __atuvc=2%7C48; intercom-id-rsodlit1=bad16bb0-0d8a-4de1-b7d0-4412cb277075; wooTracker=bhMtogmHMTUg; fs_uid=www.fullstory.com`1WAJR`6330646235447296:5681097123823616`222312`; ajs_group_id=null; _ga=GA1.2.1999935515.1512042170; _gid=GA1.2.1540975249.1512647730; ajs_user_id=222312; amplitude_idstackshare.io=eyJkZXZpY2VJZCI6IjQ1OGU1NDk2LWU5ODctNDBjNi04MDQxLWIyZDZmMjkwYTljY1IiLCJ1c2VySWQiOiIyMjIzMTIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1MTI3MzkyNjkwODQsImxhc3RFdmVudFRpbWUiOjE1MTI3NDI1MDY2NzYsImV2ZW50SWQiOjE5NywiaWRlbnRpZnlJZCI6NjUsInNlcXVlbmNlTnVtYmVyIjoyNjJ9; uvts=6pNGSSEwGigBIJEJ; intercom-session-rsodlit1=N1VsRlVld2xsbURLWVZpMURITDMxNUM2NkJoY3VBOGhsMTJEVkJhMTgxWlpjSmpYUDdrNGhwTndHdkh3ZVRRTS0tVWQwcXY1eERkSFBYTCtKWWdRMVhtUT09--c34f5c040bafb8f6059848d8ecbcdf42d1e94ce7; intercom-lou-rsodlit1=1; XSRF-TOKEN=pzu7cLRmOTVWDF0WeyoEN8KFuOHQOMrVknF0gZP5RcDnLsphbDMuHVFEasWIpZ%2Fosd8jZt7j85MEqAslb84TAg%3D%3D; _stackshare_production_session=M0ppSHpZUFNnUzhWbnlyNjFOdHA1NTh4dnljcVc2V1BKVXFleHovVjU3QitvQjJIbzI1cFZrcXZsZklYb3RXYkZPR21SZk93dlp1MHJXR080TUJLb0pNSTRpdmxoam1xTlVNcjlJeER1L1ZCQWJNalFMYnpDcFU2MHNXS3ZsQW5TUUZhZnAxalJXVitjK3lDUmdVMGZtNXNOWDkxczBwSzBQeFhyMWtRTjQ5MlllRUN1UnFWVlIvUFl3LzgvdE84dWcrNHRtMDBlQTdWVWFob3Yyd1FUQ0VQc3pzVVB1NFRISWd4TnFVTktZZkFvRkFGRDh3ZmxjUXJGdUdxQnV4MENzakJsaGIzWFVENnlIODdRdG1jcmlJT3BNdWh1MURkdkZLVjdtZkRaODQ9LS1QZWt1Q1pxbnY5VHpWUmVmWHZod0xRPT0%3D--c99c145b46d7c59d1faa73cff4b74cabbfcee641; _gat=1'}
        response = requests.get(constants.DOMAIN + self.__app_url + '/in-stacks', headers=headers)
        companies = ""
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            text = soup.find('a', id='service-stacks-load-more')
            if text is None:
                raise InvalidValueException(msg='cannot get %s id, cookie may expired ' % self.__app_url)
            app_id = text['data-service-id']
            payload = {'page': 1, 'service_id': app_id}
            url = constants.DOMAIN + '/service-stacks-load-more'
            page = requests.post(url, data=payload)
            while page.text:
                detail_soup = BeautifulSoup(page.text, 'lxml')
                for label in detail_soup.find_all('a'):
                    companies = companies + '|' + label['data-hint']
                payload['page'] = payload['page'] + 1
                page = requests.post(url, data=payload)
            return companies
        else:
            return None

    @classmethod
    def __check_url(cls, app_url):
        if app_url is None:
            raise InvalidValueException(msg='app_url cannot be null')
        if cls.response:
            return cls.response
        else:
            cls.response = requests.get(constants.DOMAIN + app_url)
            return cls.response
