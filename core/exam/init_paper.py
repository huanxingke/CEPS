# coding=utf8
"""
生成试卷
"""
import time

from core.exam.calculate_leakage import setGasLeakage, setFluidLeakage
from core.exam.calculate_pool import setPoolQuestion
from core.exam.calculate_potency import setPotency
from core.exam.calculate_Q import setQ
from core.exam.calculate_wastewater import setWasteWaterQuestion
from core.exam.set_choices import setChoices, setJudgement
from core.exam.set_completions import setCompletions


def initPaper(amount=30, seed=None, correct=False):
    """生成试卷

    :param amount: 题量 30/60/90
    :param seed: 随机数种子
    :param correct: 是否需要答案
    :return:
    """
    # 设置随机数种子
    if seed is None:
        seed = int(time.time() * 10 ** 6)
    origin_seed = seed
    # 各题型数量
    choices_amount = int(10 * amount / 30)
    judgement_amount = int(10 * amount / 30)
    completions_amount = int(5 * amount / 30)
    leakage_amount = int(amount / 30)
    pool_amount = int(amount / 30)
    potency_amount = int(amount / 30)
    Q_amount = int(amount / 30)
    waste_water_amount = int(amount / 30)
    examinee_answer = {}
    correct_answer = {}
    # 选择题
    choices_questions = []
    examinee_answer["choices"] = {}
    correct_answer["choices"] = {}
    while len(choices_questions) < choices_amount:
        choices_question, choices_options, choices_answer = setChoices(seed=seed)
        if choices_question not in [i["question"] for i in choices_questions]:
            choices_questions.append({
                "question": choices_question,
                "options": choices_options
            })
            examinee_answer["choices"][f"choices-{len(choices_questions) - 1}"] = []
            correct_answer["choices"][f"choices-{len(choices_questions) - 1}"] = [choices_options.index(i) for i in choices_answer]
        seed += 1
    # 判断题
    judgement_questions = []
    examinee_answer["judgement"] = {}
    correct_answer["judgement"] = {}
    while len(judgement_questions) < judgement_amount:
        judgement_question, judgement_explanation, judgement_answer = setJudgement(seed=seed)
        if judgement_question not in [i["question"] for i in judgement_questions]:
            judgement_questions.append({
                "question": judgement_question
            })
            examinee_answer["judgement"][f"judgement-{len(judgement_questions) - 1}"] = 0
            correct_answer["judgement"][f"judgement-{len(judgement_questions) - 1}"] = 0 if judgement_answer == "错误" else 1
        seed += 1
    # 填空题
    completions_questions = []
    examinee_answer["completions"] = {}
    correct_answer["completions"] = {}
    while len(completions_questions) < completions_amount:
        completions_question, completions_blanks, completions_answer = setCompletions(seed=seed)
        if completions_question not in [i["question"] for i in completions_questions]:
            completions_questions.append({
                "question": completions_question,
                "blanks": completions_blanks
            })
            for blank_index in range(completions_blanks):
                examinee_answer["completions"][f"completions-{len(completions_questions) - 1}-{blank_index}"] = ""
                correct_answer["completions"][f"completions-{len(completions_questions) - 1}-{blank_index}"] = completions_answer[blank_index]
        seed += 1
    # 企业 Q 值计算
    Q_questions = []
    examinee_answer["Q"] = {}
    correct_answer["Q"] = {}
    while len(Q_questions) < Q_amount:
        Q_question, Q_explanation, Q_answer = setQ(seed=seed)
        if Q_question not in [i["question"] for i in Q_questions]:
            Q_questions.append({
                "question": Q_question,
                "explanation": Q_explanation
            })
            examinee_answer["Q"][f"Q-{len(Q_questions) - 1}"] = 0.00
            correct_answer["Q"][f"Q-{len(Q_questions) - 1}"] = Q_answer
        seed += 1
    # 泄漏量计算
    leakage_questions = []
    examinee_answer["leakage"] = {}
    correct_answer["leakage"] = {}
    while len(leakage_questions) < leakage_amount:
        if len(leakage_questions) % 2 != 0:
            leakage_question, leakage_explanation, leakage_answer = setGasLeakage(seed=seed)
        else:
            leakage_question, leakage_explanation, leakage_answer = setFluidLeakage(seed=seed)
        if leakage_question not in [i["question"] for i in leakage_questions]:
            leakage_questions.append({
                "question": leakage_question
            })
            examinee_answer["leakage"][f"leakage-{len(leakage_questions) - 1}"] = 0.00
            correct_answer["leakage"][f"leakage-{len(leakage_questions) - 1}"] = leakage_answer
        seed += 1
    # 事故应急池计算
    pool_questions = []
    examinee_answer["pool"] = {}
    correct_answer["pool"] = {}
    while len(pool_questions) < pool_amount:
        pool_question, pool_explanation, pool_answer = setPoolQuestion(seed=seed)
        if pool_question not in [i["question"] for i in pool_questions]:
            pool_questions.append({
                "question": pool_question,
                "explanation": pool_explanation
            })
            examinee_answer["pool"][f"pool-{len(pool_questions) - 1}"] = 0.00
            correct_answer["pool"][f"pool-{len(pool_questions) - 1}"] = pool_answer
        seed += 1
    # 消防废水计算
    waste_water_questions = []
    examinee_answer["waste_water"] = {}
    correct_answer["waste_water"] = {}
    while len(waste_water_questions) < waste_water_amount:
        waste_water_question, waste_water_explanation, waste_water_answer1, waste_water_answer2, no_outdoor = setWasteWaterQuestion(seed=seed)
        if waste_water_question not in [i["question"] for i in waste_water_questions]:
            waste_water_questions.append({
                "question": waste_water_question,
                "explanation": waste_water_explanation,
                "no_outdoor": no_outdoor
            })
            examinee_answer["waste_water"][f"waste_water-{len(waste_water_questions) - 1}-1"] = 0.00
            correct_answer["waste_water"][f"waste_water-{len(waste_water_questions) - 1}-1"] = waste_water_answer1
            if not no_outdoor:
                examinee_answer["waste_water"][f"waste_water-{len(waste_water_questions) - 1}-2"] = 0.00
                correct_answer["waste_water"][f"waste_water-{len(waste_water_questions) - 1}-2"] = waste_water_answer2
        seed += 1
    # 落地浓度计算
    potency_questions = []
    examinee_answer["potency"] = {}
    correct_answer["potency"] = {}
    while len(potency_questions) < potency_amount:
        potency_question, potency_explanation, potency_answer1, potency_answer2, potency_answer3 = setPotency(seed=seed)
        if potency_question not in [i["question"] for i in potency_questions]:
            potency_questions.append({
                "question": potency_question,
                "explanation": potency_explanation
            })
            examinee_answer["potency"][f"potency-{len(potency_questions) - 1}-1"] = 0.00
            examinee_answer["potency"][f"potency-{len(potency_questions) - 1}-2"] = 0.00
            examinee_answer["potency"][f"potency-{len(potency_questions) - 1}-3"] = 0.00
            correct_answer["potency"][f"potency-{len(potency_questions) - 1}-1"] = potency_answer1
            correct_answer["potency"][f"potency-{len(potency_questions) - 1}-2"] = potency_answer2
            correct_answer["potency"][f"potency-{len(potency_questions) - 1}-3"] = potency_answer3
        seed += 1
    # 试卷
    paper = {
        "choices_questions": choices_questions,
        "judgement_questions": judgement_questions,
        "completions_questions": completions_questions,
        "Q_questions": Q_questions,
        "leakage_questions": leakage_questions,
        "pool_questions": pool_questions,
        "waste_water_questions": waste_water_questions,
        "potency_questions": potency_questions,
        "seed": origin_seed,
        "amount": amount
    }
    if not correct:
        return paper, examinee_answer
    else:
        return paper, correct_answer
