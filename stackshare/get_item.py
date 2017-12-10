# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

from stackshare import constants


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
        except Exception as e:
            print(e)
        finally:
            return eval(ids)
    else:
        return ids


# 通过app_id获取 url 和 app_name
def get_item(ids=None, url_category=None):
    res = []
    if ids is None or url_category is None:
        return None
    datasource = {'ids[]': []}
    for app_id in ids:
        datasource['ids[]'].append(app_id)
    req = requests.post(constants.DOMAIN + url_category + '/load-more', data=datasource)
    soup = BeautifulSoup(req.text, 'lxml')
    for data in soup.find_all('div', 'thumbnail-home'):
        res.append({
            'url': data.find('a')['href'],
            'name': data.find('span', itemprop='keywords').get_text()
        })
    return res

if __name__ == '__main__':
    print(get_item([18, 1171], '/application_and_data'))
