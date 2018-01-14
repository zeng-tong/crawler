import asyncio

import aiohttp

from config import GetLogger, mysql_session
from stackshare.src.Service.CompanyService import CompanyService
from stackshare.src.Utils import constants
from stackshare.src.Utils.utils import loop
from bs4 import BeautifulSoup

logger = GetLogger('company').get_logger()


class Company:
    total = 0
    retry_list = []

    @classmethod
    async def fetch(cls, url, headers):
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url=url, headers=headers) as response:
                text = await response.text()
                cnt = cls.get_companies(text)
                if cnt == 0:
                    cls.retry_list.append(url)
                cls.total += cnt
                logger.info('Page %s has %d persisted into mysql.' % (url.replace(constants.DOMAIN + '/companies?page=', ''), cnt))

    def retry(self, headers):
        urls = self.retry_list
        self.retry_list = []
        retry_task = []
        for url in urls:
            retry_task.append(self.fetch(url=url,
                                         headers=headers))
            logger.info('Page %s putted into retry task.' % url.replace(constants.DOMAIN + '/companies?page=', ''))
        loop.run_until_complete(asyncio.gather(*retry_task))

    def start(self):
        import time
        start = time.time()
        headers = {'Cookie': 'ajs_anonymous_id=%22a1aad3a2-0df8-41f8-9ca0-b61008d9f68d%22; __uvt=; __atuvc=2%7C48; intercom-id-rsodlit1=bad16bb0-0d8a-4de1-b7d0-4412cb277075; wooTracker=bhMtogmHMTUg; fs_uid=www.fullstory.com`1WAJR`6330646235447296:5681097123823616`222312`; ajs_group_id=null; _ga=GA1.2.1999935515.1512042170; _gid=GA1.2.1540975249.1512647730; ajs_user_id=222312; amplitude_idstackshare.io=eyJkZXZpY2VJZCI6IjQ1OGU1NDk2LWU5ODctNDBjNi04MDQxLWIyZDZmMjkwYTljY1IiLCJ1c2VySWQiOiIyMjIzMTIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1MTI3MzkyNjkwODQsImxhc3RFdmVudFRpbWUiOjE1MTI3NDI1MDY2NzYsImV2ZW50SWQiOjE5NywiaWRlbnRpZnlJZCI6NjUsInNlcXVlbmNlTnVtYmVyIjoyNjJ9; uvts=6pNGSSEwGigBIJEJ; intercom-session-rsodlit1=N1VsRlVld2xsbURLWVZpMURITDMxNUM2NkJoY3VBOGhsMTJEVkJhMTgxWlpjSmpYUDdrNGhwTndHdkh3ZVRRTS0tVWQwcXY1eERkSFBYTCtKWWdRMVhtUT09--c34f5c040bafb8f6059848d8ecbcdf42d1e94ce7; intercom-lou-rsodlit1=1; XSRF-TOKEN=pzu7cLRmOTVWDF0WeyoEN8KFuOHQOMrVknF0gZP5RcDnLsphbDMuHVFEasWIpZ%2Fosd8jZt7j85MEqAslb84TAg%3D%3D; _stackshare_production_session=M0ppSHpZUFNnUzhWbnlyNjFOdHA1NTh4dnljcVc2V1BKVXFleHovVjU3QitvQjJIbzI1cFZrcXZsZklYb3RXYkZPR21SZk93dlp1MHJXR080TUJLb0pNSTRpdmxoam1xTlVNcjlJeER1L1ZCQWJNalFMYnpDcFU2MHNXS3ZsQW5TUUZhZnAxalJXVitjK3lDUmdVMGZtNXNOWDkxczBwSzBQeFhyMWtRTjQ5MlllRUN1UnFWVlIvUFl3LzgvdE84dWcrNHRtMDBlQTdWVWFob3Yyd1FUQ0VQc3pzVVB1NFRISWd4TnFVTktZZkFvRkFGRDh3ZmxjUXJGdUdxQnV4MENzakJsaGIzWFVENnlIODdRdG1jcmlJT3BNdWh1MURkdkZLVjdtZkRaODQ9LS1QZWt1Q1pxbnY5VHpWUmVmWHZod0xRPT0%3D--c99c145b46d7c59d1faa73cff4b74cabbfcee641; _gat=1'}
        fail_cnt = 0
        try:
            tasks = []
            for page in range(1, 635):
                tasks.append(self.fetch(url=constants.DOMAIN + '/companies?page=%d' % page,
                                        headers=headers))
                logger.info('Page %d has put in schedule' % page)
            loop.run_until_complete(asyncio.gather(*tasks))
            fail_cnt = len(self.retry_list)
            self.retry(headers)
        except Exception as e:
            logger.error(e)
            # retry 之前抛异常
            if fail_cnt == 0:
                fail_cnt = len(self.retry_list)
        finally:
            logger.info('%d pages retried once ,%d pages failed of all 634 pages. Once-done rate %f '
                        % (fail_cnt,
                           len(self.retry_list),
                           1 - ((fail_cnt + len(self.retry_list)) / 634)))
            logger.info('All pages retrieved done.')
            end = time.time()
            logger.info('%d had retrieved into MySQL and Cost %f sec' % (self.total, (end - start)))
            logger.info('QPS is %f' % (self.total / (end - start)))


    @classmethod
    def get_companies(cls, text):
        _soup = BeautifulSoup(text, 'lxml')
        _stacks = _soup.find_all('div', id='stack-card')
        for _stack in _stacks:
            cls.persist(CompanyService(_stack).get_info())
        return len(_stacks)

    @classmethod
    def persist(cls, entity):
        try:
            session = mysql_session()
            session.expunge_all()
            session.add(entity)
            session.commit()
            logger.info(msg='Company 「%s」 save to mysql succeed...' % (entity.name))
        except Exception as e:
            logger.error(e)
            logger.error(msg='Company 「%s」 insert error.Please noticing.' % (entity.name))
        finally:
            session.close()

if __name__ == '__main__':
    Company().start()
        # headers = {'Cookie': 'ajs_anonymous_id=%22a1aad3a2-0df8-41f8-9ca0-b61008d9f68d%22; __uvt=; __atuvc=2%7C48; intercom-id-rsodlit1=bad16bb0-0d8a-4de1-b7d0-4412cb277075; wooTracker=bhMtogmHMTUg; fs_uid=www.fullstory.com`1WAJR`6330646235447296:5681097123823616`222312`; ajs_group_id=null; _ga=GA1.2.1999935515.1512042170; _gid=GA1.2.1540975249.1512647730; ajs_user_id=222312; amplitude_idstackshare.io=eyJkZXZpY2VJZCI6IjQ1OGU1NDk2LWU5ODctNDBjNi04MDQxLWIyZDZmMjkwYTljY1IiLCJ1c2VySWQiOiIyMjIzMTIiLCJvcHRPdXQiOmZhbHNlLCJzZXNzaW9uSWQiOjE1MTI3MzkyNjkwODQsImxhc3RFdmVudFRpbWUiOjE1MTI3NDI1MDY2NzYsImV2ZW50SWQiOjE5NywiaWRlbnRpZnlJZCI6NjUsInNlcXVlbmNlTnVtYmVyIjoyNjJ9; uvts=6pNGSSEwGigBIJEJ; intercom-session-rsodlit1=N1VsRlVld2xsbURLWVZpMURITDMxNUM2NkJoY3VBOGhsMTJEVkJhMTgxWlpjSmpYUDdrNGhwTndHdkh3ZVRRTS0tVWQwcXY1eERkSFBYTCtKWWdRMVhtUT09--c34f5c040bafb8f6059848d8ecbcdf42d1e94ce7; intercom-lou-rsodlit1=1; XSRF-TOKEN=pzu7cLRmOTVWDF0WeyoEN8KFuOHQOMrVknF0gZP5RcDnLsphbDMuHVFEasWIpZ%2Fosd8jZt7j85MEqAslb84TAg%3D%3D; _stackshare_production_session=M0ppSHpZUFNnUzhWbnlyNjFOdHA1NTh4dnljcVc2V1BKVXFleHovVjU3QitvQjJIbzI1cFZrcXZsZklYb3RXYkZPR21SZk93dlp1MHJXR080TUJLb0pNSTRpdmxoam1xTlVNcjlJeER1L1ZCQWJNalFMYnpDcFU2MHNXS3ZsQW5TUUZhZnAxalJXVitjK3lDUmdVMGZtNXNOWDkxczBwSzBQeFhyMWtRTjQ5MlllRUN1UnFWVlIvUFl3LzgvdE84dWcrNHRtMDBlQTdWVWFob3Yyd1FUQ0VQc3pzVVB1NFRISWd4TnFVTktZZkFvRkFGRDh3ZmxjUXJGdUdxQnV4MENzakJsaGIzWFVENnlIODdRdG1jcmlJT3BNdWh1MURkdkZLVjdtZkRaODQ9LS1QZWt1Q1pxbnY5VHpWUmVmWHZod0xRPT0%3D--c99c145b46d7c59d1faa73cff4b74cabbfcee641; _gat=1'}
        # resp = requests.get(constants.DOMAIN + '/companies?page=%d' % 1, headers=headers)
        # soup = BeautifulSoup(resp.text, 'lxml')
        # stacks = soup.find_all('div', id='stack-card')
        # for stack in stacks:
        #     print(stack)
