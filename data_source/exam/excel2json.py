# coding=utf8
"""
将 《事故案例与题目》 excel 转为 json
"""
import json

import xlrd


def readExcel(excel_path, sheet_index, columns_index):
    """读 excel"""
    excel = xlrd.open_workbook(excel_path)
    sheet = excel.sheets()[sheet_index]
    columns = []
    for i in columns_index:
        column = sheet.col_values(colx=i, start_rowx=1, end_rowx=None)
        columns.append(column)
    return columns


def date_as_datetime(date):
    """将 excel 读来的日期转换为正常日期形式"""
    new_date = xlrd.xldate_as_datetime(date, 0).strftime("%Y-%m-%d")
    return new_date


def initCases():
    """生成: 事故案例 json"""
    excel_path = "./static/事故案例与题目.xlsx"
    cases_list = readExcel(excel_path=excel_path, sheet_index=0, columns_index=range(9))
    cases = []
    for case_index, case in enumerate(cases_list[0]):
        name = case
        when = date_as_datetime(cases_list[1][case_index])
        where = cases_list[2][case_index]
        who = cases_list[3][case_index]
        event = cases_list[4][case_index]
        keywords = cases_list[5][case_index]
        emergency_response = cases_list[6][case_index]
        emergency_management_evaluation = cases_list[7][case_index]
        onsite_disposal_evaluation = cases_list[8][case_index]
        cases.append({
            "name": name,
            "when": when,
            "where": where,
            "who": who,
            "event": event,
            "keywords": keywords,
            "emergency_response": emergency_response,
            "emergency_management_evaluation": emergency_management_evaluation,
            "onsite_disposal_evaluation": onsite_disposal_evaluation,
            "index": case_index
        })
    with open("./static/cases.json", "w", encoding="utf-8") as fp:
        json.dump(cases, fp)


def initCompletions():
    """生成: 填空题 json"""
    excel_path = "./static/事故案例与题目.xlsx"
    completions_list = readExcel(excel_path=excel_path, sheet_index=1, columns_index=[0, 1])
    completions = []
    for question_index, question in enumerate(completions_list[0]):
        answer_str = str(completions_list[1][question_index])
        answer = answer_str.split("；")
        completions.append({
            "question": question,
            "answer": answer
        })
    with open("./static/completions.json", "w", encoding="utf-8") as fp:
        json.dump(completions, fp)


def initChoices():
    """生成: 选择题 json"""
    excel_path = "./static/事故案例与题目.xlsx"
    choices_list = readExcel(excel_path=excel_path, sheet_index=2, columns_index=[0, 1, 2])
    choices = []
    for question_index, question in enumerate(choices_list[0]):
        option = str(choices_list[1][question_index]).split("；")
        answer = str(choices_list[2][question_index]).split("；")
        answer_ = []
        # 去除浮点数形式
        for i in answer:
            i = i.replace(".0", "")
            answer_.append(str(i))
        option = [i.replace("~", "～").replace(" ", "") for i in option]
        option = [i for i in option if i]
        answer_ = [i.replace("~", "～").replace(" ", "") for i in answer_]
        answer_ = [i for i in answer_ if i]
        choices.append({
            "question": question,
            "option": option,
            "answer": answer_
        })
    with open("./static/choices.json", "w", encoding="utf-8") as fp:
        json.dump(choices, fp)


def initPlans():
    """生成: 应急演练 json"""
    excel_path = "./static/事故案例与题目.xlsx"
    plans_list = readExcel(excel_path=excel_path, sheet_index=3, columns_index=range(9))
    plans = []
    for theme_index, theme in enumerate(plans_list[0]):
        chemical_types = plans_list[1][theme_index]
        former_periods = plans_list[2][theme_index].split("\n")
        command_centre = plans_list[3][theme_index].split("\n")
        engineering_team = plans_list[4][theme_index].split("\n")
        methods = plans_list[5][theme_index].split("\n")
        alert_team = plans_list[6][theme_index].split("\n")
        medical_team = plans_list[7][theme_index].split("\n")
        after_periods = plans_list[8][theme_index].split("\n")
        plans.append({
            "theme": theme,
            "chemical_types": chemical_types,
            "former_periods": [i for i in former_periods if i],
            "command_centre": [i for i in command_centre if i],
            "engineering_team": [i for i in engineering_team if i],
            "methods": [i for i in methods if i],
            "alert_team": [i for i in alert_team if i],
            "medical_team": [i for i in medical_team if i],
            "after_periods": [i for i in after_periods if i],
        })
    with open("./static/plans.json", "w", encoding="utf-8") as fp:
        json.dump(plans, fp)
