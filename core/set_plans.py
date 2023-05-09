# coding=utf8
"""
核心 API: 生成应急演练题目
"""
import random
import json
import os

from conf.path import json_path


with open(os.path.join(json_path, "plans.json"), "r", encoding="utf-8") as fp:
    plans = json.load(fp)


def setPlans():
    """生成应急演练题目"""
    # 生成主题字典
    themes = {}
    # 选项
    options_titles = ["former_periods", "command_centre", "engineering_team", "methods", "alert_team", "medical_team", "after_periods"]
    options_dict = {}
    for options_title in options_titles:
        options_dict[options_title] = []
    for plan in plans:
        # 主题
        theme = plan["theme"]
        # 涉及的危化品
        chemical_types = plan["chemical_types"]
        for options_title in options_titles:
            options = plan[options_title]
            for option in options:
                if option and (option not in options_dict[options_title]):
                    options_dict[options_title].append(option)
        # 构造成字典嵌列表形式
        if theme not in themes:
            themes[theme] = []
        themes[theme].append(chemical_types)
    for options_title in options_titles:
        random.shuffle(options_dict[options_title])
    return themes, options_dict, plans
