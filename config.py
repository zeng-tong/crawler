# -*- coding: utf-8 -*-
import logging

import sys

import datetime


class GetLogger:

    def __init__(self, name):
        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(filename='stackshare/log/%s_%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d'), name), mode='a+')
        stream_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)

    def get_logger(self):
        return self.__logger
