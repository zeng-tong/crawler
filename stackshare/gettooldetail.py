#! -*-utf-8-*-
import requests
from bs4 import BeautifulSoup
import re

DOMIN = 'https://stackshare.io'



def gettooldetail(toolname = None):

    toolpage = requests.get(DOMIN +toolname).text

    # 需要获取的信息
    # 1.name,2.explain,3.son_label,4.second_label,5.papa_label,6.star_count,7.votes_count,8.fans_count,9.company using it

    soup = BeautifulSoup(toolpage,"lxml")

    #print(soup.prettify())




    #get explain imformation

    link = soup.find_all('span')

    explain = re.search(r'.*alternativeHeadline.*<',str(link),re.M).group()

    explain = re.sub(r'.*=', "", explain)

    explain = re.sub(r'<.*',"",explain,2)

    explain = re.sub(r'.*>',"",explain)

    print(explain)



    #get son_label

    all_label = re.search(r'itemprop=.*span>',str(link),re.M).group()

    son_label = re.sub(r'<.*',"",all_label)

    son_label = re.sub(r'.*>',"",son_label)

    print(son_label)


    # get second_label

    list = all_label.split(',')

    second_label = list[1]

    second_label = re.search(r'>.*<',str(second_label),re.M).group()

    second_label = re.sub('>|<',"",second_label)

    print(second_label)



    #get papa_label

    papa_label = list[2]

    papa_label = re.search(r'>.*<',str(papa_label),re.M).group()

    papa_label = re.sub('>|<',"",papa_label)

    print(papa_label)


    #get star_count

    star_count = soup.find(id = "service-1101")

    star_count = re.search('>\d+<',str(star_count),re.M).group()

    star_count = re.sub('>|<', "", star_count)

    print(star_count)


    # #get votes_count
    # ncount = soup.find_all('a')
    # star_count = re.search(r'Rating.*k',str(ncount),re.M).group()
    # print(star_count)



res = gettooldetail('/bootstrap')



