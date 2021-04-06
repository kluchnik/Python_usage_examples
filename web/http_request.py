'''
--------------------
Модуль для отправики GET-запросов и POST-запросов
--------------------
import http_request
--------------------
'''

import re, requests, urllib3


class Traget():
    def __init__():
        self.__parameters = {
            'protocol': 'https',
            'address': 'ya.ru',
            'port': '443',
            'urn': '/',
            'timeout': 10
            }
	self.__auth_method = None
        self.__auth_parameters = {
            'login': '',
            'password': ''
            }

    def set_parameters(self, **kwarg):
        '''
        Установить параметры
        example-1: <class>.set_parameters(ip='192.168.1.11', login='root', password='12345678')
        example-2: <class>.set_parameters(**{'ip':'192.168.1.11', 'login':'root', 'password':'12345678'})
        '''
        for item in kwarg.keys():
            self.__parameters[item] = kwarg[item]
