# -*- coding:utf-8 -*-
__author__ = 'xwk'
import os
class ServerException(Exception):
    """ 服务器内部错误 """
    pass

print os.getcwd()