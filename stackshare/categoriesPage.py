#! -*-utf-8-*-
import requests
from bs4 import BeautifulSoup
import re

DOMIN = 'https://stackshare.io'


# def get_categories(category=None):
#
#     if category is None:
#         category = '/categories'
#
#     categories_page = requests.get(DOMIN + category)
#
#     html = categories_page.text
#
#     soup = BeautifulSoup(html, "lxml")
#
#     li = soup.find('li', 'hide-4')
#
#     div = li.find('div', 'navmenu')
#
#     res = []
#     for url in div.find_all('a'):
#         res.append(url['href'])
#     return res
#
#
# def get_apps_ids(url_category=None):
#     if url_category is None:
#         return []
#     category_html = requests.get(DOMIN + url_category).text
#
#     soup = BeautifulSoup(category_html, 'lxml')
#
#     all_script = soup.find_all(re.compile('^script'))
#
#     ids_script = re.search(r'ordered_service_ids.*]', str(all_script), re.M).group()  # ordered_service_ids = [...]
#
#     ids = re.sub('.*=', "", ids_script)
#
#     return eval(ids)
#
# res = get_apps_ids('/application_and_data')
# print(res)
# print(len(res))


def gettooldetail(toolname = None):

    toolpage = requests.get(DOMIN +toolname).text

    soup = BeautifulSoup(toolpage,"lxml")
    #print(soup.prettify())

    # 需要获取的信息
    # 1.name,2.explain,3.son_label,4.second_label,5.papa_label,6.star_count,7.votes_count,8.fans_count,9.company using it


    #get explain imformation
    link = soup.find_all('span')
    explain = re.search(r'.*alternativeHeadline.*<',str(link),re.M).group()
    explain = re.sub(r'.*=', "", explain)
    explain = re.sub(r'<.*',"",explain,2)
    explain = re.sub(r'.*>',"",explain)
    print(explain)

    #get son_label
    #son_label = re.search(r'.*name.*>',str(link),re.M).group()
    #print(son_label)

res = gettooldetail('/bootstrap')



