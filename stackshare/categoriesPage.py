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


def get_apps_ids(url_category=None):
    if url_category is None:
        return []
    category_html = requests.get(constants.DOMAIN + url_category).text

    soup = BeautifulSoup(category_html, 'lxml')

    ids = re.search(r'ordered_service_ids = (.*)?]', soup.text, re.M).group(0).replace('ordered_service_ids = ', '')

    return eval(ids)


