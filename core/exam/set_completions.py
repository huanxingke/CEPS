# coding=utf8
"""
填空题
"""
import random
import json
import re
import os

from conf.path import json_exam_path


with open(os.path.join(json_exam_path, "completions.json"), "r", encoding="utf-8") as fp:
    completions = json.load(fp)


def setCompletions(seed=None):
    """填空题"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    completion = random.choice(completions)
    question = completion["question"]
    answer = completion["answer"]
    # 空格数
    blanks = len(list(set(re.compile(r"（(\d)）").findall(question))))
    return question, blanks, answer