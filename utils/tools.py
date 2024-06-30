'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-29 20:11:12
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-30 15:27:50
FilePath: /Code/BicameralMind/utils/tools.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
import tomli, yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
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

def calculate_cosine_similarity(text1, text2):
    # 创建TF-IDF向量化器
    vectorizer = TfidfVectorizer()
    
    # 将文本转换为TF-IDF向量
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    
    # 计算余弦相似度
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    
    return cosine_sim[0][0]
