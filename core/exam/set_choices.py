# coding=utf8
"""
选择题与判断题
"""
import random
import json
import re
import os

from conf.path import json_exam_path


with open(os.path.join(json_exam_path, "choices.json"), "r", encoding="utf-8") as fp:
    choices = json.load(fp)


def setChoices(seed=None):
    """选择题"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    choice = random.choice(choices)
    question = choice["question"]
    option = choice["option"]
    answer = choice["answer"]
    # 打乱选项顺序
    shuffle_option = option[:]
    random.shuffle(shuffle_option)
    return question, shuffle_option, answer


def setJudgement(seed=None):
    """判断题"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    choice = random.choice(choices)
    question = choice["question"]
    option = choice["option"]
    answer = choice["answer"]
    question_no_blank = question
    # 随机选择一个选项
    random_option = random.choice(option)
    for i in random_option.split("、"):
        # 逐个替换掉 （）
        question_no_blank = question_no_blank.replace("（）", i, 1)
    new_answer = "错误"
    # 如果随机选到的选项就是正确答案
    if random_option in answer:
        new_answer = "正确"
    return question_no_blank, None, new_answer
