# coding=utf8
"""
核心 API: 检索环境风险事故案例
"""
import json
import os

from gensim import corpora, models, similarities
import streamlit as st
import jieba

from conf.path import models_cases_path


class QueryCases(object):
    def __init__(self, cases):
        self.cases = cases
        # 加载索引字典
        self.dictionary = corpora.Dictionary.load(os.path.join(models_cases_path, "cases.dictionary"))
        # 加载模型
        self.tfidf = models.TfidfModel.load(os.path.join(models_cases_path, "cases.tfidf"))
        # 加载相似度对象
        self.index = similarities.MatrixSimilarity.load(os.path.join(models_cases_path, "cases.index"))

    def query(self, keywords):
        """检索案例

        :param keywords: 关键词
        :return: 相关度最高的 10 个搜索结果[列表]
        """
        # 处理
        keywords = jieba.lcut(keywords)
        # 生成搜索词袋
        keywords_corpus = self.dictionary.doc2bow(keywords)
        # 转换为TF-IDF主题向量
        keywords_vec = self.tfidf[keywords_corpus]
        # 计算相似度
        sim = self.index[self.tfidf[keywords_vec]]
        # 排序以获取相似度结果
        sim_sorted = [i for i in sorted(enumerate(sim), key=lambda item: -item[1]) if i[1] != 0]
        # 从总数据中检索
        query_results = []
        for i in sim_sorted:
            case_index, case_sim = i
            query_result = self.cases[case_index]
            query_result["similarity"] = float(case_sim)
            query_result["index"] = int(case_index)
            query_results.append(query_result)
        # 返回搜索结果
        return query_results[:10]