'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-29 20:11:12
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-29 20:15:38
FilePath: /Code/BicameralMind/utils/tools.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
import tomli, yaml
def config_parse(config_path):
    if config_path.split(".")[-1] == 'toml':
        with open(config_path, 'rb') as f:
            config_data = tomli.load(f)
    elif config_path.split(".")[-1] == 'yaml':
        with open(config_path, 'r', encoding='utf-8') as stream:
            config_data = yaml.safe_load(stream)
    else:
        raise ValueError("Config format not supported, please use toml or yaml")
    return config_data