# coding=utf8
"""
批改试卷
"""
import copy
import os

from matplotlib import font_manager
import matplotlib.pyplot as plt
import streamlit as st

from conf.path import fonts_path
from core.exam.init_paper import initPaper


def gradePaper(examinee_answer_compress):
    """批改试卷

    :param examinee_answer_compress: 压缩后的examinee
    :return:
    """
    examinee_answer_list = examinee_answer_compress["answer"]
    seed = examinee_answer_compress["seed"]
    amount = examinee_answer_compress["amount"]
    # 获取原试卷与正确答案
    paper, correct_answer = initPaper(amount=amount, seed=seed, correct=True)
    # 批改后的答案
    grade_answer = copy.deepcopy(correct_answer)
    # 将正确答案也同样压缩
    correct_answer_list = [list(i.values()) for i in list(correct_answer.values())]
    # 获取所有题目编号
    question_keys = [list(i.keys()) for i in list(correct_answer.values())]
    # 得分
    grades = {
        # 试卷总分
        "total": 0,
        # 考生实际得分
        "examinee": 0,
        # 考生百分制得分
        "hundred": 0,
        # 每部分得分
        "choices": 0,
        "judgement": 0,
        "completions": 0,
        "Q": 0,
        "leakage": 0,
        "pool": 0,
        "waste_water": 0,
        "potency": 0
    }
    # 选择题
    examinee_choices_answers = examinee_answer_list[0]
    correct_choices_answers = correct_answer_list[0]
    for examinee_choices_answer_index, examinee_choices_answer in enumerate(examinee_choices_answers):
        choices_grade = 0
        correct_choices_answer = correct_choices_answers[examinee_choices_answer_index]
        if sorted(correct_choices_answer) == sorted(examinee_choices_answer):
            choices_grade = 5
        else:
            for choices_answer in examinee_choices_answer:
                if choices_answer not in correct_choices_answer:
                    choices_grade = 0
                    break
                else:
                    choices_grade += 1
            if choices_grade > 5:
                choices_grade = 5
        grades["total"] += 5
        grades["examinee"] += choices_grade
        grades["choices"] += choices_grade
        grade_answer["choices"][question_keys[0][examinee_choices_answer_index]] = {
            "points": choices_grade,
            "examinee": examinee_choices_answer,
            "correct": correct_choices_answer
        }
    # 判断题
    examinee_judgement_answers = examinee_answer_list[1]
    correct_judgement_answers = correct_answer_list[1]
    for examinee_judgement_answer_index, examinee_judgement_answer in enumerate(examinee_judgement_answers):
        judgement_grade = 0
        correct_judgement_answer = correct_judgement_answers[examinee_judgement_answer_index]
        if correct_judgement_answer == examinee_judgement_answer:
            judgement_grade += 2
        grades["total"] += 2
        grades["examinee"] += judgement_grade
        grades["judgement"] += judgement_grade
        grade_answer["judgement"][question_keys[1][examinee_judgement_answer_index]] = {
            "points": judgement_grade,
            "examinee": examinee_judgement_answer,
            "correct": correct_judgement_answer
        }
    # 填空题
    examinee_completions_answers = examinee_answer_list[2]
    correct_completions_answers = correct_answer_list[2]
    for examinee_completions_answer_index, examinee_completions_answer in enumerate(examinee_completions_answers):
        completions_grade = 0
        correct_completions_answer = correct_completions_answers[examinee_completions_answer_index]
        if correct_completions_answer == examinee_completions_answer:
            completions_grade += 2
        grades["total"] += 2
        grades["examinee"] += completions_grade
        grades["completions"] += completions_grade
        grade_answer["completions"][question_keys[2][examinee_completions_answer_index]] = {
            "points": completions_grade,
            "examinee": examinee_completions_answer,
            "correct": correct_completions_answer
        }
    # 计算填空题的计算结果
    # 误差在正负 15% 以内都可以
    error = 0.15
    # 企业 Q 值计算
    examinee_Q_answers = examinee_answer_list[3]
    correct_Q_answers = correct_answer_list[3]
    for examinee_Q_answer_index, examinee_Q_answer in enumerate(examinee_Q_answers):
        Q_grade = 0
        correct_Q_answer = correct_Q_answers[examinee_Q_answer_index]
        if (abs(examinee_Q_answer - correct_Q_answer) / correct_Q_answer) <= error:
            Q_grade += 10
        grades["total"] += 10
        grades["examinee"] += Q_grade
        grades["Q"] += Q_grade
        grade_answer["Q"][question_keys[3][examinee_Q_answer_index]] = {
            "points": Q_grade,
            "examinee": examinee_Q_answer,
            "correct": correct_Q_answer
        }
    # 泄漏量计算
    examinee_leakage_answers = examinee_answer_list[4]
    correct_leakage_answers = correct_answer_list[4]
    for examinee_leakage_answer_index, examinee_leakage_answer in enumerate(examinee_leakage_answers):
        leakage_grade = 0
        correct_leakage_answer = correct_leakage_answers[examinee_leakage_answer_index]
        if (abs(examinee_leakage_answer - correct_leakage_answer) / correct_leakage_answer) <= error:
            leakage_grade += 10
        grades["total"] += 10
        grades["examinee"] += leakage_grade
        grades["leakage"] += leakage_grade
        grade_answer["leakage"][question_keys[4][examinee_leakage_answer_index]] = {
            "points": leakage_grade,
            "examinee": examinee_leakage_answer,
            "correct": correct_leakage_answer
        }
    # 事故应急池计算
    examinee_pool_answers = examinee_answer_list[5]
    correct_pool_answers = correct_answer_list[5]
    for examinee_pool_answer_index, examinee_pool_answer in enumerate(examinee_pool_answers):
        pool_grade = 0
        correct_pool_answer = correct_pool_answers[examinee_pool_answer_index]
        if (abs(examinee_pool_answer - correct_pool_answer) / correct_pool_answer) <= error:
            pool_grade += 10
        grades["total"] += 10
        grades["examinee"] += pool_grade
        grades["pool"] += pool_grade
        grade_answer["pool"][question_keys[5][examinee_pool_answer_index]] = {
            "points": pool_grade,
            "examinee": examinee_pool_answer,
            "correct": correct_pool_answer
        }
    # 消防废水计算
    examinee_waste_water_answers = examinee_answer_list[6]
    correct_waste_water_answers = correct_answer_list[6]
    for examinee_waste_water_answer_index, examinee_waste_water_answer in enumerate(examinee_waste_water_answers):
        waste_water_grade = 0
        correct_waste_water_answer = correct_waste_water_answers[examinee_waste_water_answer_index]
        if (abs(examinee_waste_water_answer - correct_waste_water_answer) / correct_waste_water_answer) <= error:
            waste_water_grade += 10
        grades["total"] += 10
        grades["examinee"] += waste_water_grade
        grades["waste_water"] += waste_water_grade
        grade_answer["waste_water"][question_keys[6][examinee_waste_water_answer_index]] = {
            "points": waste_water_grade,
            "examinee": examinee_waste_water_answer,
            "correct": correct_waste_water_answer
        }
    # 落地浓度计算
    examinee_potency_answers = examinee_answer_list[7]
    correct_potency_answers = correct_answer_list[7]
    for examinee_potency_answer_index, examinee_potency_answer in enumerate(examinee_potency_answers):
        potency_grade = 0
        correct_potency_answer = correct_potency_answers[examinee_potency_answer_index]
        if (abs(examinee_potency_answer - correct_potency_answer) / correct_potency_answer) <= error:
            potency_grade += 10
        grades["total"] += 10
        grades["examinee"] += potency_grade
        grades["potency"] += potency_grade
        grade_answer["potency"][question_keys[7][examinee_potency_answer_index]] = {
            "points": potency_grade,
            "examinee": examinee_potency_answer,
            "correct": correct_potency_answer
        }
    grades["hundred"] = round(grades["examinee"] * 100 / grades["total"], 1)
    return grades, grade_answer


def showGrades(grades):
    """显示分数

    :param grades: 由 gradePaper 函数返回的 grades
    :return:
    """
    # 加载字体
    font = font_manager.FontProperties(
        fname=os.path.join(fonts_path, "楷体_GB2312.ttf"),
        size=12
    )
    projects_Chinese = ["总分", "考生得分", "选择题", "判断题", "填空题", "Q值计算", "泄漏量计算", "事故应急池计算", "消防废水计算", "落地浓度计算"]
    projects = ["total", "examinee", "choices", "judgement", "completions", "Q", "leakage", "pool", "waste_water", "potency"]
    projects_grades = [grades[i] for i in projects]
    ax = plt.gca()
    for major_locator in [i * 10 for i in range(1, 6)]:
        if projects_grades[0] // major_locator <= 10:
            ax.xaxis.set_major_locator(plt.MultipleLocator(major_locator))
            break
    ax.invert_yaxis()
    plt.yticks(fontproperties=font)
    rects = plt.barh(projects_Chinese, projects_grades, height=0.3)
    for rect in rects:
        width = rect.get_width()
        plt.text(width + 1, rect.get_y() + rect.get_height() / 2, width, va="center")
    st.pyplot(fig=plt)
