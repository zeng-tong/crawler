# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from stackshare.src.exceptions import InvalidValueException

from config import GetLogger
from stackshare.src import constants


class PicGetter:
    @classmethod
    def get_apps_icon_by_ids(cls, ids=None, category=None):
        if ids is None:
            raise InvalidValueException(msg='id cannot be null')
        if category is None:
            raise InvalidValueException(msg='No category, cannot load page')
        datasource = {'ids[]': []}
        for app_id in ids:
            datasource['ids[]'].append(app_id)
        req = requests.post(constants.DOMAIN + category + '/load-more', data=datasource)
        soup = BeautifulSoup(req.text, 'lxml')
        for content in soup.find_all('div', 'thumbnail-home'):
            pic_name = content.find('span', itemprop='keywords').get_text()
            pic_url = content.find('a', 'hint--top').find('img')['src']
            cls.__fetch_pic(url=pic_url, pic_name=pic_name + '.jpg', path=constants.STACK_PIC_PATH + '/')

    @staticmethod
    def __fetch_pic(url=None, pic_name=None, path=None):
        logger = GetLogger(__name__).get_logger()
        if url is None:
            return None
        if path is None:
            path = constants.RESOURCE_PATH
        response = requests.get(url)
        try:
            if response.status_code == 200:
                with open(path + pic_name, 'wb') as f:
                    f.write(response.content)
                    f.close()
                    # print('download %s succeed' % pic_name)
                    logger.info('download %s succeed' % pic_name)

        except Exception as e:
            # print('download %s error: ' % pic_name + str(e))
            logger.warn('download %s error: ' % pic_name + str(e))

