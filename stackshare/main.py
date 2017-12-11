# -*- coding: utf-8 -*-
import threading

import sys

import getopt

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


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hpc", ["producer", "consumer"])
    except getopt.GetoptError:
        print('usage: main.py -p # producer mode')
        print(      ' main.py -c # consumer mode')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--producer"):
            print('producer start working...')
            try:
                # consumer.start()
                t1 = threading.Thread(target=producer.start)
                t2 = threading.Thread(target=producer.start)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception as e:
                print(e)
        elif opt in ("-c", "--consumer"):
            print('consumer start working...')
            try:
                # producer.start()
                t1 = threading.Thread(target=crawl)
                t2 = threading.Thread(target=crawl)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception as e:
                print(e)
    # TODO 将category 放进 QUEUE


if __name__ == '__main__':
    main(sys.argv[1:])
