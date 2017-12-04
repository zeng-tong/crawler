import requests
from bs4 import BeautifulSoup
import re

DOMIN = 'https://stackshare.io'


def get_categories(category=None):

    if category is None:
        category = '/categories'

    categories_page = requests.get(DOMIN + category)

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
    category_html = requests.get(DOMIN + url_category).text

    soup = BeautifulSoup(category_html, 'lxml')

    all_script = soup.find_all(re.compile('^script'))

    ids_script = re.search(r'ordered_service_ids.*]', str(all_script), re.M).group()  # ordered_service_ids = [...]

    ids = re.sub(r'.*=', "", ids_script)

    return eval(ids)

print(get_apps_ids('/application_and_data'))


