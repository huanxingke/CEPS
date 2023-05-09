# coding=utf8
"""
事故应急池计算
"""
import random
import json
import os

from conf.path import json_exam_path


with open(os.path.join(json_exam_path, "rainfalls.json"), "r", encoding="utf-8") as fp:
    rainfalls = json.load(fp)


# ***** V1: 收集系统范围内发生事故的物料量, m^3 ***** #
def setV1():
    # 铁路槽车容量, m3
    railway_tanker_capacity = [50, 60]
    # 汽车罐车, m3
    car_tanker_capacity = [5, 10, 15, 20, 25, 30]
    # 储罐容量, m3
    storage_tanker_capacity = [1, 3, 5, 10, 15, 20, 25, 30, 40, 50, 80, 100, 150]
    # 反应器或中间储罐, m3
    reactor_capacity = [1, 2, 3, 4, 5]
    types = range(0, 4)
    capacities = [railway_tanker_capacity, car_tanker_capacity, storage_tanker_capacity, reactor_capacity]
    type_index = random.choice(types)
    capacity = random.choice(capacities[type_index])
    # V1, m3
    V1 = capacity
    return [V1, type_index]


# ***** V2: 发生事故的储罐、装置或铁路、汽车装卸区的消防水量, m^3 ***** #
def setV2(V1):
    # 给水流量, L/s
    if V1 >= 50:
        flow_range = [200 + i * 10 for i in range(11)]
        area_range = [i * 1000 for i in range(20, 31)]
    elif V1 >= 20:
        flow_range = [100 + i * 10 for i in range(11)]
        area_range = [i * 1000 for i in range(15, 21)]
    else:
        flow_range = [60 + i * 10 for i in range(4)]
        area_range = [i * 1000 for i in range(10, 16)]
    # 厂区面积, m2
    area = random.choice(area_range)
    # 火灾延续时间, h
    duration_range = range(3, 6)
    # 流量, L/s
    flow = random.choice(flow_range)
    # t, h
    duration = random.choice(duration_range)
    # V2, m3
    V2 = flow * duration * 3600 / 1000
    return [round(V2, 2), flow, duration, area]


# ***** V3: 发生事故时可以转输到其他储存或处理设施的物料量, m^3 ***** #
def setV3(V1):
    # 这里只考虑围堰的情况, m3
    cofferdam = random.choice([True, False])
    if cofferdam:
        V3 = V1
    else:
        V3 = 0
    return [V3, cofferdam]


# ***** V4: 发生事故时仍必须进入该收集系统的生产废水量, m^3 ***** #
def setV4():
    # 这里假定发生事故时停止生产, m3
    V4 = 0
    return V4


# ***** V5: 发生事故时仍可能进入该收集系统的降雨量, m^3 ***** #
def setV5(area):
    # 降雨数据
    location = random.choice(rainfalls)
    city = location["location"]
    rainfall_steps = int((location["rainfall"][1] - location["rainfall"][0]) / 10)
    rainfall_range = [location["rainfall"][0] + i * 10 for i in range(rainfall_steps + 1)]
    days_steps = location["days"][1] - location["days"][0]
    days_range = [location["days"][0] + i for i in range(days_steps + 1)]
    # 年降雨量, mm
    rainfall = random.choice(rainfall_range)
    # 天数
    days = random.choice(days_range)
    # V5, m3
    V5 = 10 * (rainfall / days) * area / (10 ** 4)
    return [round(V5, 2), city, rainfall, days]


def setPoolQuestion(seed=None):
    """事故应急池计算"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    V1, type_index = setV1()
    V2, flow, duration, area = setV2(V1=V1)
    V3, cofferdam = setV3(V1=V1)
    V4 = setV4()
    V5, city, rainfall, days = setV5(area=area)
    V = round(V1 + V2 - V3 + V4 + V5, 2)
    question = f"现有位于{city}的某化工厂，厂房面积${area}m^3$，厂内储存有可燃液体，并运行着相关的生产工艺。\n某天，"
    if type_index == 0:
        question += f"该工厂的卸车区正在进行着装卸工作，一容积为${V1}m^3$的满载的槽车发生可燃液体泄露起火事故。"
    elif type_index == 1:
        question += f"该工厂的卸车区正在进行着装卸工作，一容积为${V1}m^3$的满载的罐车发生可燃液体泄露起火事故。"
    elif type_index == 2:
        question += f"厂内一容积为${V1}m^3$装有可燃液体的满载的储罐发生泄露起火事故。"
    else:
        question += f"该工厂生产车间一容积为${V1}m^3$的满载的可燃液体反应釜发生泄露起火事故。"
    question += f"\n该工厂立即启动应急预案，开展消防工作，并以${flow}L/s$的消防水流量进行灭火以及降温。\n${duration}h$后，火势彻底扑灭，消防给水停止。"
    question += f"\n灭火过程中，发生泄漏的罐体内物料已全部流出，但由于该工厂设有事故应急池，消防废水全部收集于应急池内，"
    if cofferdam:
        question += "并且发生泄漏事故的区域设有符合规范的围堰，泄露物无向外扩散的情况，"
    else:
        question += f"并且泄漏物也全部进入了应急池，"
    question += "该起事故未造成环境污染。"
    question += "\n假设本次事故发生后，该工厂立刻停止了生产工艺，停止产生生产废水。"
    question += "处理事故时，未有其他废水或者其他泄漏物进入事故应急池。"
    question += "事故结束后，事故应急池内废水也未外溢。"
    question += f"\n已知该工厂所在地区年降雨量为${rainfall}mm$，降雨天数为{days}天。"
    question += "\n试计算该工厂的事故应急池的容量最小可能是多少？\n（计算中间数据以及最终结果均保留小数点后两位，单位为$m^3$）"
    calculation_process = "解析：\n"
    calculation_process += f"（1）由于物料满载且全部泄露，则发生事故的物料量即发生泄露的罐体容积：\n$$\nV_1={V1}m^3\n$$\n"
    calculation_process += f"（2）然后确定消防水量：\n$$\nV_2={flow}\\times{duration}\\times3600/1000={V2}m^3\n$$\n"
    if cofferdam:
        calculation_process += f"（3）由于设置有围堰，泄漏物将全部截流于围堰内：\n$$\nV_3={V3}m^3\n$$\n"
    else:
        calculation_process += f"（3）由于泄漏物全部进入了应急池：\n$$\nV_3={V3}m^3\n$$\n"
    calculation_process += f"（4）并且事故发生后，该工厂停止了生产工艺，无生产废水产生：\n$$\nV_4={V4}m^3\n$$\n"
    calculation_process += f"（5）根据厂区面积以及该地区的降雨数据：\n$$\nV_5=(10\\times{rainfall}/{days})\\times{area}/10^4={V5}m^3\n$$\n"
    calculation_process += f"（6）综上，该工厂事故应急池最小容积为：\n$$\nV={V1}+{V2}-{V3}+{V4}+{V5}={V}m^3\n$$"
    return question, calculation_process, V
