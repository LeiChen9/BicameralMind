'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-28 08:07:32
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-28 08:09:19
FilePath: /Code/BicameralMind/data_structures/io_object.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''

import json

class IOObject(object):
    def __init__(self, params: dict):
        self.__params = params
        for k, v in params.items():
            self.__dict__[k] = v

    def to_dict(self):
        return self.__params

    def to_json_str(self):
        return json.dumps(self.__params)

    def add_data(self, key, value):
        self.__params[key] = value
        self.__dict__[key] = value

    def get_data(self, key, default=None):
        return self.__params.get(key, default)
