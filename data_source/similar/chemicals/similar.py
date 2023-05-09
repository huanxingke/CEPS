# coding=utf8
"""
生成化学品检索模型
"""
import re

from gensim import corpora, models, similarities
import string
import jieba
import json


# 去停用词
def drop_stop_words(stopWords, words):
    res = []
    for w in words:
        if w not in stopWords:
            res.append(w)
    return res


# 加载题库
with open("chemicals.json", "r") as fp:
    chemicals_data = json.load(fp)

# 处理每种化学品名称
chemical_names = []
for chemical in chemicals_data:
    chemical_dict = []
    for cas_number in chemical["cas_number"]:
        if cas_number not in chemical_dict:
            chemical_dict.append(cas_number)
    for name in chemical["name"]:
        for w in jieba.lcut(name):
            if w not in chemical_dict:
                chemical_dict.append(w)
    chemical_names.append(chemical_dict)

# 生成索引字典
dictionary = corpora.Dictionary(chemical_names)
# 保存字典
dictionary.save("chemicals.dictionary")
# 加载字典
# dictionary = corpora.Dictionary.load("tiku.dictionary")

# 生成化学品名称词袋
corpus = [dictionary.doc2bow(text) for text in chemical_names]

# 建立TF-IDF模型
tfidf = models.TfidfModel(corpus)
# 保存模型
tfidf.save("chemicals.tfidf")
# 加载模型
# tfidf = models.TfidfModel.load("chemicals.tfidf")

# 转换为TF-IDF主题向量
documents = tfidf[corpus]
# 生成相似度对象
index = similarities.SparseMatrixSimilarity(documents, num_features=len(dictionary.keys()))
# 保存相似度对象
index.save("chemicals.index")
# 加载相似度对象
# index = similarities.MatrixSimilarity.load('tiku.index')

# 要搜索的题目
query = "氨"
# 处理
query = jieba.lcut(query)
# 生成搜索词袋
query_corpus = dictionary.doc2bow(query)
# 转换为TF-IDF主题向量
query_vec = tfidf[query_corpus]

# 计算相似度
sim = index[tfidf[query_vec]]

# 排序以获取相似度结果
sim_sorted = sorted(enumerate(sim), key=lambda item: -item[1])

# 从总数据中检索
query_results = []
for i in sim_sorted:
    chemical_index, chemical_sim = i
    query_result = chemicals_data[chemical_index]
    query_result["similarity"] = chemical_sim
    query_results.append(query_result)

print(query_results[0])