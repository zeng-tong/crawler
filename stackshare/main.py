# -*- coding: utf-8 -*-
import threading

from stackshare import consumer, producer

from stackshare.src import get_item

categories = get_item.get_categories()

# if __name__ == '__main__':
#     print('there are %s categories: ' % len(categories))
#     index = -1
#     for category in categories:
#         print('%s. %s' % (++index, category))
#     i = input()
#     consume = consumer.start(categories[i])


def crawl():
    for category in categories:
        consumer.start(category)

if __name__ == '__main__':
    try:
        producer.start()
        t1 = threading.Thread(target=crawl)
        t2 = threading.Thread(target=crawl)
        t1.start()
        t2.start()

        t1.join()
        t2.join()
    except Exception as e:
        print(e)

# TODO 将category 放进 QUEUE
