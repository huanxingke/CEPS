# coding=utf8
"""
生成环境风险案例检索模型
"""
from gensim import corpora, models, similarities
import codecs
import jieba
import json


# 去停用词
def drop_stop_words(stopWords, words):
    res = []
    for i in words:
        if i not in stopWords:
            res.append(i)
    return res


# 加载案例
with open("cases.json", "r", encoding="utf-8") as fp:
    cases_data = json.load(fp)

# 加载停用词
stop_words = codecs.open("stop_words.txt", encoding="utf-8").readlines()
stop_words = [word.replace("\n", "").strip() for word in stop_words]

# 处理每个案例
cases = []
for case in cases_data:
    del case["when"]
    del case["index"]
    case_details = []
    for case_detail in case.values():
        case_detail = jieba.lcut(case_detail)
        case_detail = drop_stop_words(stopWords=stop_words, words=case_detail)
        for cd in case_detail:
            if cd not in case_details:
                case_details.append(cd)
    cases.append(case_details)

# 生成索引字典
dictionary = corpora.Dictionary(cases)
# 保存字典
dictionary.save("cases.dictionary")
# 加载字典
# dictionary = corpora.Dictionary.load("cases.dictionary")

# 生成词袋
corpus = [dictionary.doc2bow(text) for text in cases]

# 建立TF-IDF模型
tfidf = models.TfidfModel(corpus)
# 保存模型
tfidf.save("cases.tfidf")
# 加载模型
# tfidf = models.TfidfModel.load("cases.tfidf")

# 转换为TF-IDF主题向量
documents = tfidf[corpus]
# 生成相似度对象
index = similarities.SparseMatrixSimilarity(documents, num_features=len(dictionary.keys()))
# 保存相似度对象
index.save("cases.index")
# 加载相似度对象
# index = similarities.MatrixSimilarity.load("cases.index")