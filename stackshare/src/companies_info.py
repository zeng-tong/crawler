import requests
from bs4 import BeautifulSoup

from config import PyRedis
from stackshare.models.companies import Companies
from stackshare.src import constants
from stackshare.src.exceptions import InvalidValueException


class CompaniesInfo:

    def __init__(self, app_url):
        self.__app_url = app_url
        self.redis = PyRedis().get_resource()

    def companies(self):
        result = self.__companies()
        companies = []
        page = next(result)
        while page:
            for company in page:
                companies.append(Companies(company_name=company['company'], logo=company['logo']))
            yield companies
            page = next(result)

    def __companies(self):
        companies = []
        headers = {'Cookie': 'ajs_anonymous_id=%22a1aad3a2-0df8-41f8-9ca0-b61008d9f68d%22; __uvt=; __atuvc=2%7C48; intercom-id-rsodlit1=bad16bb0-0d8a-4de1-b7d0-4412cb277075; wooTracker=bhMtogmHMTUg; fs_uid=www.fullstory.com`1WAJR`6330646235447296:5681097123823616`222312`; ajs_group_id=null; _ga=GA1.2.1999935515.1512042170; _gid=GA1.2.1540975249.1512647730; ajs_user_id=222312; amplitude_idstackshare.io=eyJkZXZpY2VJZCI6IjQ1OGU1NDk2LWU5ODctNDBjNi04MDQxLWIyZDZmMjkwYTljY1IiLCJ1c2VySWQiOiIyMjIzMTIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1MTI3MzkyNjkwODQsImxhc3RFdmVudFRpbWUiOjE1MTI3NDI1MDY2NzYsImV2ZW50SWQiOjE5NywiaWRlbnRpZnlJZCI6NjUsInNlcXVlbmNlTnVtYmVyIjoyNjJ9; uvts=6pNGSSEwGigBIJEJ; intercom-session-rsodlit1=N1VsRlVld2xsbURLWVZpMURITDMxNUM2NkJoY3VBOGhsMTJEVkJhMTgxWlpjSmpYUDdrNGhwTndHdkh3ZVRRTS0tVWQwcXY1eERkSFBYTCtKWWdRMVhtUT09--c34f5c040bafb8f6059848d8ecbcdf42d1e94ce7; intercom-lou-rsodlit1=1; XSRF-TOKEN=pzu7cLRmOTVWDF0WeyoEN8KFuOHQOMrVknF0gZP5RcDnLsphbDMuHVFEasWIpZ%2Fosd8jZt7j85MEqAslb84TAg%3D%3D; _stackshare_production_session=M0ppSHpZUFNnUzhWbnlyNjFOdHA1NTh4dnljcVc2V1BKVXFleHovVjU3QitvQjJIbzI1cFZrcXZsZklYb3RXYkZPR21SZk93dlp1MHJXR080TUJLb0pNSTRpdmxoam1xTlVNcjlJeER1L1ZCQWJNalFMYnpDcFU2MHNXS3ZsQW5TUUZhZnAxalJXVitjK3lDUmdVMGZtNXNOWDkxczBwSzBQeFhyMWtRTjQ5MlllRUN1UnFWVlIvUFl3LzgvdE84dWcrNHRtMDBlQTdWVWFob3Yyd1FUQ0VQc3pzVVB1NFRISWd4TnFVTktZZkFvRkFGRDh3ZmxjUXJGdUdxQnV4MENzakJsaGIzWFVENnlIODdRdG1jcmlJT3BNdWh1MURkdkZLVjdtZkRaODQ9LS1QZWt1Q1pxbnY5VHpWUmVmWHZod0xRPT0%3D--c99c145b46d7c59d1faa73cff4b74cabbfcee641; _gat=1'}
        # get company id
        response = requests.get(constants.DOMAIN + self.__app_url + '/in-stacks', headers=headers)
        company_soup = BeautifulSoup(response.text, 'lxml')
        text = company_soup.find('a', id='service-stacks-load-more')
        if text is None:
            raise InvalidValueException(msg='cannot get %s id, cookie may expired ' % self.__app_url)

        for each in company_soup.find('div', 'companies-using-service').find_all('div', 'col-md-1 stack-logo'):
            companies.append({'company': each.find('img')['alt'], 'logo': each.find('img')['src']})

        app_id = text['data-service-id']

        # request data page by page.
        page = self.redis.hget('companies_page', self.__app_url)

        # if not exist means it's the first time to run the category.
        page = int(page) if page else 1
        payload = {'page': page, 'service_id': app_id}

        url = constants.DOMAIN + '/service-stacks-load-more'
        page = requests.post(url, data=payload)
        while page.text:
            detail_soup = BeautifulSoup(page.text, 'lxml')
            for each in detail_soup.find_all('div', 'col-md-1 stack-logo'):
                companies.append({'company': each.find('img')['alt'], 'logo': each.find('img')['src']})
            yield companies

            # 避免下次重复插入
            companies = []

            payload['page'] = payload['page'] + 1
            self.redis.hset('companies_page', self.__app_url, payload['page'])
            page = requests.post(url, data=payload)
