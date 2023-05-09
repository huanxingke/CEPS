# coding=utf8
"""
企业 Q 值计算
"""
import random
import json
import os

from conf.path import json_exam_path


with open(os.path.join(json_exam_path, "critical-quantity.json"), "r", encoding="utf-8") as fp:
    chemicals = json.load(fp)


def setQ(seed=None):
    """企业 Q 值计算"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    # 每次取 4~6 种物质
    chosen_length = random.randint(4, 6)
    chosen_chemicals = random.sample(chemicals, chosen_length)
    # 设定 Q 值为 0.5 ~ 1.5, 保留小数点后两位
    Q = round(random.uniform(0.5, 1.5), 2)
    # 设定每种物质的 Q 即 Qi
    # 即需要将 Q 分为 chosen_length 个 Qi 之和
    # 设定 Qi > 0.1 Q
    Qis = []
    Q_ = Q * 1
    for i in range(1, chosen_length):
        Qi = round(random.uniform(0.1 * Q_, (10 - chosen_length + i) * 0.1 * Q_), 2)
        Q_ -= Qi
        Qis.append(Qi)
    Qis.append(round(Q_, 2))
    random.shuffle(Qis)

    chemicals_with_amount = []
    for chemical_index, chemical in enumerate(chosen_chemicals):
        critical_quantity = chemical["critical_quantity"]
        # 设置物质的总量
        amount = round(Qis[chemical_index] * critical_quantity, 2)
        # 重新计算 Qi
        Qi = round(amount / critical_quantity, 2)
        chemical["amount"] = amount
        chemical["Qi"] = Qi
        chemicals_with_amount.append(chemical)

    question = "某企业厂界内存在以下物质，计算该企业的Q值。（计算中间数据以及最终结果均保留小数点后两位）\n| 序号 | 名称 | 项目最大储存情况 |\n| :----: | :----: | :----: |\n"
    calculation_process = "解析：\n"
    result = "（%s）综上，计算得：\n$$\nQ=" % (chosen_length + 1)
    cal_Q = 0
    for chemical_index, chemical in enumerate(chemicals_with_amount):
        name = chemical["name"]
        critical_quantity = chemical["critical_quantity"]
        amount = chemical["amount"]
        Qi = chemical["Qi"]
        calculation_process += "（%s）查得%s的临界量：\n$$\nQ_{%s}=%st\n$$\n" % (chemical_index + 1, name, name, critical_quantity)
        # 小于 0.1 的在题目中换算为 kg
        if amount > 0.1:
            question += "| {} | {} | {}（t） |\n".format(chemical_index + 1, name, amount)
            calculation_process += "则$Q_i$为：\n$$\nQ_{i,%s}=\\frac{q_{%s}}{Q_{%s}}=\\frac{%s}{%s}=%s\n$$\n" % (
                name, name, name, amount, critical_quantity, Qi
            )
        else:
            question += "| {} | {} | {}（kg） |\n".format(chemical_index + 1, name, amount * 1000)
            calculation_process += "则$Q_i$为：\n$$\nQ_{i,%s}=\\frac{q_{%s}}{Q_{%s}}=\\frac{%s/1000}{%s}=%s\n$$\n" % (
                name, name, name, amount * 1000, critical_quantity, Qi
            )
        result += "Q_{i,%s}+" % name
        cal_Q += Qi
    cal_Q = round(cal_Q, 2)
    result = result.strip("+") + "=%s\n$$" % cal_Q
    calculation_process += result
    return question, calculation_process, cal_Q
