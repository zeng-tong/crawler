# -*- coding: utf-8 -*-
import threading

import sys

import getopt

from stackshare import consumer, producer
from stackshare.consumer import consume
from stackshare.producer import produce

from stackshare.src import get_item

from config import GetLogger

# if __name__ == '__main__':
#     print('there are %s categories: ' % len(categories))
#     index = -1
#     for category in categories:
#         print('%s. %s' % (++index, category))
#     i = input()
#     consume = consumer.start(categories[i])



def main(argv):
    logger = GetLogger(__name__).get_logger()
    try:
        opts, args = getopt.getopt(argv, "pc", ["producer", "consumer"])
    except getopt.GetoptError:
        print('usage: main.py -p')
        print('       main.py -c')
        print('-p producer ,-c consumer')
        sys.exit(2)
    if len(opts) == 0:
        print('usage: main.py -p')
        print('       main.py -c')
        print('-p producer ,-c consumer')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--producer"):
            logger.info(msg='producer start working...')
            try:
                t1 = threading.Thread(target=produce().start)
                t2 = threading.Thread(target=produce().start)
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception as e:
                print(e)
        elif opt in ("-c", "--consumer"):
            logger.info(msg='consumer start working...')
            try:
                t1 = threading.Thread(target=consume().start())
                t2 = threading.Thread(target=consume().start())
                t1.start()
                t2.start()
                t1.join()
                t2.join()
            except Exception as e:
                print(e)
    # TODO 将category 放进 QUEUE


if __name__ == '__main__':
    main(sys.argv[1:])
