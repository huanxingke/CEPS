# coding=utf8
"""
泄漏量计算
"""
import random


def setFluidLeakage(seed=None):
    """液体泄露"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    # 密度, 0.7 ~ 1.4 Kg/m3
    rho = random.choice([i * 0.01 for i in range(70, 140)])
    rho = round(rho, 2)
    # 环境大气压, kPa
    p_0 = 101.325
    # 容器内介质压力(绝压), kPa
    p = round(random.choice(range(50, 1101)) + p_0, 2)
    # 泄漏口面积, cm2
    A = random.choice(range(1, 15))
    # 排放系数类型
    C_d_types = [
        {
            "type": "薄壁",
            "value": 0.62
        },
        {
            "type": "厚壁",
            "value": 0.81
        },
        {
            "type": "修圆",
            "value": 1.0
        },
        {
            "type": "圆形",
            "value": [0.65, 0.50]
        },
        {
            "type": "多边形",
            "value": [0.65, 0.50]
        },
        {
            "type": "三角形",
            "value": [0.60, 0.45]
        },
        {
            "type": "长条形",
            "value": [0.55, 0.40]
        },
    ]
    chosen_C_d_type = random.choice(C_d_types)
    C_d_type = chosen_C_d_type["type"]
    # 排放系数
    C_d = chosen_C_d_type["value"]
    # 雷诺数
    Re = 0
    question = ""
    # 管道中泄露
    if C_d_type[-1] == "形":
        # 泄漏口上液位高度, m
        h_mm = random.choice(range(10, 51))
        h = h_mm * 10 ** (-3)
        Re = random.choice([i * 5 for i in range(10, 31)])
        if Re > 100:
            C_d = C_d[0]
        else:
            C_d = C_d[1]
        question += "现有一化工厂，其中一管道中输送着某种均匀混合流体，"
        question += "流体密度为${}kg/m^3$，管道内绝压为${}kPa$。".format(rho, p)
        question += "某天，该管道发生了破裂，管内流体通过一{}小孔泄露。".format(C_d_type)
        question += "泄露开始时泄漏口上液位高度为${}mm$，环境大气压为${}kPa$，重力加速度取$9.8m/s^2$。".format(h_mm, p_0)
        question += "若泄漏口面积为${}cm^2$，求泄漏流量。（计算结果单位为$kg/s$，保留两位小数）".format(A)
    # 储罐内泄露
    else:
        # 泄漏口上液位高度, m
        h_cm = random.choice(range(5, 51))
        h = h_cm * 0.1
        question += "现有一化工厂，其中一储罐中存储着某种均匀混合流体，"
        question += "流体密度为${}kg/m^3$，储罐内绝压为${}kPa$。".format(rho, p)
        question += "某天，该储罐发生了破裂，罐内流体通过一{}小孔泄露。".format(C_d_type)
        question += "泄露开始时泄漏口上液位高度为${}cm$，环境大气压为${}kPa$，重力加速度取$9.8m/s^2$。".format(h_cm, p_0)
        question += "若泄漏口面积为${}cm^2$，求泄漏流量。（计算结果单位为$kg/s$，保留小数点后两位）".format(A)
    answer = C_d * A * (10 ** (-4)) * ((2 * (p - p_0) * (10 ** 3) / rho + 2 * 9.8 * h) ** 0.5)
    answer = round(answer, 2)
    return question, None, answer


def setGasLeakage(seed=None):
    """气体泄漏"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    # 容器内介质压力(绝压), MPa
    p = round(random.choice(range(8, 16)) * 0.1 + 101.325 * 10 ** (-3), 2)
    # 泄漏口面积, cm2
    A = random.choice(range(1, 15))
    # 排放系数类型
    C_d_types = [
        {
            "type": "圆形",
            "value": 1.00
        },
        {
            "type": "三角形",
            "value": 0.95
        },
        {
            "type": "长方形",
            "value": 0.90
        }
    ]
    chosen_C_d_type = random.choice(C_d_types)
    C_d_type = chosen_C_d_type["type"]
    # 排放系数
    C_d = chosen_C_d_type["value"]
    # 储存的气体
    gases = [
        {
            "name": "H_2",
            "y": 1.410,
            "M": 2
        },
        {
            "name": "N_2",
            "y": 1.402,
            "M": 28
        },
        {
            "name": "H_2",
            "y": 1.410,
            "M": 2
        },
        {
            "name": "O_2",
            "y": 1.397,
            "M": 32
        },
        {
            "name": "H_2",
            "y": 1.410,
            "M": 2
        },
        {
            "name": "SO_2",
            "y": 1.272,
            "M": 64
        },
        {
            "name": "NH_3",
            "y": 1.313,
            "M": 17
        },
        {
            "name": "C_2H_2",
            "y": 1.235,
            "M": 26
        },
        {
            "name": "C_2H_4",
            "y": 1.249,
            "M": 28
        },
        {
            "name": "CH_4",
            "y": 1.314,
            "M": 16
        }
    ]
    # 选择一种气体
    chosen_gas = random.choice(gases)
    name = chosen_gas["name"]
    y = chosen_gas["y"]
    M = chosen_gas["M"]
    question = "现有一化工厂，其中一储罐中存储着${}$，储罐内绝压为${}MPa$。".format(name, p)
    question += "某天，该储罐发生了破裂，罐内气体通过一{}小孔泄露。".format(C_d_type)
    question += "假设气体符合理想气体状态方程，容器内气体温度为$0℃$（$273.15K$），气体常数取$8.314J/(mol·K)$。"
    question += "若泄漏口面积为${}cm^2$，求泄漏流量。（计算结果单位为$g/s$，保留小数点后两位）".format(A)
    answer = C_d * A * 10 ** (-4) * p * 10 ** 6 * (y * M / 8.314 / 273.15 * (2 / (y + 1) ** ((y + 1) / (y - 1)))) * 1000
    answer = round(answer, 2)
    return question, None, answer
