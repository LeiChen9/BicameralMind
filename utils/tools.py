'''
Author: LeiChen9 chenlei9691@gmail.com
Date: 2024-06-29 20:11:12
LastEditors: LeiChen9 chenlei9691@gmail.com
LastEditTime: 2024-06-30 14:23:13
FilePath: /Code/BicameralMind/utils/tools.py
Description: 

Copyright (c) 2024 by ${chenlei9691@gmail.com}, All Rights Reserved. 
'''
import tomli, yaml
from gensim import corpora, models, similarities
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

def calculate_similarity(self, text1, text2):
    """Calculate the cosine similarity between two texts."""
    # 创建字典和语料库
    dictionary = corpora.Dictionary([text1, text2])
    corpus = [dictionary.doc2bow(text) for text in [text1, text2]]
    # 创建TF-IDF模型
    tfidf = models.TfidfModel(corpus)
    # 转换语料库为TF-IDF表示
    corpus_tfidf = tfidf[corpus]
    # 创建相似度矩阵
    index = similarities.MatrixSimilarity(corpus_tfidf)
    # 计算相似度
    similarity = index[corpus_tfidf[0]][1]
    return similarity
