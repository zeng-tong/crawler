# -*- coding: utf-8 -*-


class BaseCustomException(Exception):
    def __init__(self, msg=None, name=None):
        super(BaseCustomException, self).__init__()
        self._msg = msg
        self._name = u""

    def __str__(self):
        return "{}: msg='{}'".format(self.__class__.__name__, self._msg)

    @property
    def msg(self):
        return self._msg

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return {'error': {
            'message': self._msg
        }}


class AlreadyExistException(BaseCustomException):
    def __init__(self, msg=u'资源已存在'):
        super(AlreadyExistException, self).__init__(msg=msg)
        self._name = u'InvalidValue'


class InvalidValueException(BaseCustomException):
    def __init__(self, msg='非法的值'):
        super(InvalidValueException, self).__init__(msg=msg)
        self._name = u'InvalidValue'


class RequestErrorException(BaseCustomException):
    def __init__(self, msg=u'请求出错'):
        super(RequestErrorException, self).__init__(msg=msg)
        self._name = u'RequestError'
