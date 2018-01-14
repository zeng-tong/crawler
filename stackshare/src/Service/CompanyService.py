import requests
from bs4 import BeautifulSoup

from config import GetLogger
from stackshare.src.Utils import constants
from stackshare.src.models.company import Companies

logger = GetLogger('CompanyService').get_logger()


class CompanyService:

    def __init__(self, _soup):
        self.soup = _soup

    def name(self):
        return self.soup.find('div', 'landing-stack-name row').find('a').get_text()

    def token(self):
        return self.soup.find('div', 'landing-stack-name row').find('a')['href']

    def logo(self):
        return self.soup.find('div', 'service-logo row').find('img')['src']

    def description(self):
        return self.soup.find('div', id='companies_index__description__text').get_text()

    def site(self):
        return self.soup.find('div', id='companies_index__website_url').find('a')['href']

    def get_info(self):
        try:
            return Companies(name=str(self.name()).rstrip().lstrip(),
                             description=self.description(),
                             logo=self.logo(),
                             site=self.site(),
                             token=self.token())
        except Exception as e:
            logger.error(e)
            return None

if __name__ == '__main__':
    headers = {'Cookie': 'ajs_anonymous_id=%22a1aad3a2-0df8-41f8-9ca0-b61008d9f68d%22; __uvt=; __atuvc=2%7C48; intercom-id-rsodlit1=bad16bb0-0d8a-4de1-b7d0-4412cb277075; wooTracker=bhMtogmHMTUg; fs_uid=www.fullstory.com`1WAJR`6330646235447296:5681097123823616`222312`; ajs_group_id=null; _ga=GA1.2.1999935515.1512042170; _gid=GA1.2.1540975249.1512647730; ajs_user_id=222312; amplitude_idstackshare.io=eyJkZXZpY2VJZCI6IjQ1OGU1NDk2LWU5ODctNDBjNi04MDQxLWIyZDZmMjkwYTljY1IiLCJ1c2VySWQiOiIyMjIzMTIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1MTI3MzkyNjkwODQsImxhc3RFdmVudFRpbWUiOjE1MTI3NDI1MDY2NzYsImV2ZW50SWQiOjE5NywiaWRlbnRpZnlJZCI6NjUsInNlcXVlbmNlTnVtYmVyIjoyNjJ9; uvts=6pNGSSEwGigBIJEJ; intercom-session-rsodlit1=N1VsRlVld2xsbURLWVZpMURITDMxNUM2NkJoY3VBOGhsMTJEVkJhMTgxWlpjSmpYUDdrNGhwTndHdkh3ZVRRTS0tVWQwcXY1eERkSFBYTCtKWWdRMVhtUT09--c34f5c040bafb8f6059848d8ecbcdf42d1e94ce7; intercom-lou-rsodlit1=1; XSRF-TOKEN=pzu7cLRmOTVWDF0WeyoEN8KFuOHQOMrVknF0gZP5RcDnLsphbDMuHVFEasWIpZ%2Fosd8jZt7j85MEqAslb84TAg%3D%3D; _stackshare_production_session=M0ppSHpZUFNnUzhWbnlyNjFOdHA1NTh4dnljcVc2V1BKVXFleHovVjU3QitvQjJIbzI1cFZrcXZsZklYb3RXYkZPR21SZk93dlp1MHJXR080TUJLb0pNSTRpdmxoam1xTlVNcjlJeER1L1ZCQWJNalFMYnpDcFU2MHNXS3ZsQW5TUUZhZnAxalJXVitjK3lDUmdVMGZtNXNOWDkxczBwSzBQeFhyMWtRTjQ5MlllRUN1UnFWVlIvUFl3LzgvdE84dWcrNHRtMDBlQTdWVWFob3Yyd1FUQ0VQc3pzVVB1NFRISWd4TnFVTktZZkFvRkFGRDh3ZmxjUXJGdUdxQnV4MENzakJsaGIzWFVENnlIODdRdG1jcmlJT3BNdWh1MURkdkZLVjdtZkRaODQ9LS1QZWt1Q1pxbnY5VHpWUmVmWHZod0xRPT0%3D--c99c145b46d7c59d1faa73cff4b74cabbfcee641; _gat=1'}
    resp = requests.get(constants.DOMAIN + '/companies?page=%d' % 1, headers=headers)
    soup = BeautifulSoup(resp.text, 'lxml')
    stacks = soup.find_all('div', id='stack-card')
    for stack in stacks:
        info = CompanyService(stack).get_info()
        print(str(info.name).lstrip().rstrip())
