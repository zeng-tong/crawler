#! -*- coding: utf-8 -*-


class BaseCustomException(Exception):
    def __init__(self, msg=None, name=None):
        super(BaseCustomException, self).__init__()
        self._msg = msg
        self._name = name

    @property
    def msg(self):
        return self._msg

    @property
    def name(self):
        return self._name


class AlreadyExistException(BaseCustomException):
    def __init__(self, msg=u'资源已存在'):
        super(AlreadyExistException, self).__init__(msg=msg)
        self._name = u'InvalidValue'


class InvalidValueException(BaseCustomException):
    def __init__(self, msg='非法的值'):
        super(InvalidValueException, self).__init__(msg=msg)
        self._name = u'InvalidValue'
