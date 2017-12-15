# -*- coding: utf-8 -*-
import logging

import sys

import datetime


class GetLogger:

    def __init__(self, name):
        self.name = name

    def get_logger(self):
        file_handler = logging.FileHandler(filename='stackshare/log/%s_%s.log' % (datetime.datetime.now().strftime('%Y-%m-%d'), self.name), mode='a+')
        stream_handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='[%Y-%m-%d %H:%M:%S]',
                            handlers=[file_handler, stream_handler])
        return logging
