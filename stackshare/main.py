# -*- coding: utf-8 -*-
import getopt
import sys
import threading

from config import GetLogger
from stackshare.companies import Company
from stackshare.consumer import consume
from stackshare.producer import produce
from stackshare.src.Utils.utils import prepareCategories


def main(argv):
    logger = GetLogger(__name__).get_logger()
    try:
        opts, args = getopt.getopt(argv, "pc", ["producer", "consumer"])
    except getopt.GetoptError:
        print('usage: main.py -p')
        print('       main.py -s')
        print('       main.py -c')
        print('-p producer ,-s consumer, -c companies')
        sys.exit(2)
    if len(opts) == 0:
        print('usage: main.py -p')
        print('       main.py -s')
        print('       main.py -c')
        print('-p producer ,-s consumer, -c companies')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-p", "--producer"):
            logger.info(msg='producer start working...')
            try:
                t1 = threading.Thread(target=produce().start)
                t2 = threading.Thread(target=produce().start)
                t1.start()
                t2.start()
            except Exception as e:
                print(e)
        elif opt in ("-s", "--consumer"):
            logger.info(msg='consumer start working...')
            prepareCategories()
            try:
                t1 = threading.Thread(target=consume().start())
                t2 = threading.Thread(target=consume().start())
                t1.start()
                t2.start()
            except Exception as e:
                print(e)
        elif opt in ("-c", "--companies"):
            logger.info(msg='companies start working...')
            prepareCategories()
            try:
                Company().start()
            except Exception as e:
                print(e)
                print('Exit with exceptions')


if __name__ == '__main__':
    main(sys.argv[1:])
