# -*- coding: utf-8 -*-
import re

import requests
from bs4 import BeautifulSoup

from config import GetLogger
from stackshare.src import constants
logger = GetLogger('get_item').get_logger()


def get_categories(category=None):

        if category is None:
            category = '/categories'

        categories_page = requests.get(constants.DOMAIN + category)

        html = categories_page.text

        soup = BeautifulSoup(html, "lxml")

        li = soup.find('li', 'hide-4')

        div = li.find('div', 'navmenu')

        res = []
        for url in div.find_all('a'):
            res.append(url['href'])
        return res


# 获取一级目录下的 app_id
def get_items_ids(url_category=None):
    if url_category is None:
        return []
    response = requests.get(constants.DOMAIN + url_category)
    ids = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            ids = re.search(r'ordered_service_ids = (.*)?]', soup.text, re.M).group(0).replace('ordered_service_ids = ', '')
            ids = eval(ids)
        except Exception as e:
            print(url_category + ' cannot get app\'s ids, and had skipped.')
        finally:
            return ids
    else:
        return ids


# 通过app_id获取 url 和 app_name
def get_items(ids=None, url_category=None):

    if ids is None or url_category is None:
        return None
    datasource = {'ids[]': []}
    for app_id in ids:
        datasource['ids[]'].append(app_id)
    logger.debug(msg='Get_item: Start request ' + url_category)
    req = requests.post(constants.DOMAIN + url_category + '/load-more', data=datasource)
    logger.debug(msg='Get_item: Request ' + url_category + ' succeed')
    return get_item(req)


def get_item(response):
    soup = BeautifulSoup(response.text, 'lxml')
    res = []
    for data in soup.find_all('div', 'thumbnail-home'):
        try:
            res.append({
                'url': data.find('a')['href'],
                'name': data.find('span', itemprop='keywords').get_text()
            })
        except Exception as e:
            print(e)
            return None
    return res


if __name__ == '__main__':
    get_items([18], '/application_and_data')
