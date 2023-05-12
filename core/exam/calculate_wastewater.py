# coding=utf8
"""
消防废水计算
"""
import random
import json
import os

from conf.path import json_exam_path


with open(os.path.join(json_exam_path, "buildings.json"), "r", encoding="utf-8") as fp:
    buildings = json.load(fp)


def setDuration():
    """确定火灾持续时间"""
    chosen_building = random.choice(buildings)
    # 火灾持续时间, h
    duration = chosen_building["time"]
    # 选择建筑
    building = random.choice(chosen_building["buildings"])
    name = building["name"]
    building_description = ""
    height = 0
    if name == "工业建筑":
        building = random.choice(building["children"])
        chemicals = building["chemicals"]
        industry = building["name"][2:4]
        chemical_property = random.choice(list(chemicals.keys()))
        chemical_list = chemicals[chemical_property]
        chemical = random.choice(chemical_list)
        if industry == "厂房":
            building_description += "某涉及{}（{}）生产的{}".format(chemical, chemical_property, industry)
        else:
            building_description += "某储存有{}（{}）的{}".format(chemical, chemical_property, industry)
    elif name in ["高层建筑", "高于50m的建筑"]:
        height = random.choice(building["height"])
        building_type = random.choice(building["types"])
        building_description += "某{}，建筑高度{}m".format(building_type, height)
    elif name == "工艺装置":
        product = random.choice(building["products"])
        building_description += "某化工厂有涉及{}生产的大型工艺装置".format(product)
    else:
        building_type = random.choice(building["types"])
        building_description += "某{}".format(building_type)
    return duration, building_description, height


def setHydrantFlow():
    """确定室内外消防栓流量"""
    # 室外消防栓设计流量, L/s
    outdoor_hydrant_flow = random.choice([i * 5 for i in range(3, 9)])
    # 室内消防栓设计流量, L/s
    indoor_hydrant_flow = random.choice([i * 5 for i in range(3, 9)])
    hydrant_description = "设有室外消防栓，设计流量为${}L/s$；室内消防栓，设计流量为${}L/s$".format(outdoor_hydrant_flow, indoor_hydrant_flow)
    return [outdoor_hydrant_flow, indoor_hydrant_flow, hydrant_description]


def setMunicipalHydrantFlow():
    """确定室外市政消防栓流量"""
    municipal_hydrant_flow_description = ""
    # 是否可以不计室外消防栓流量
    no_outdoor = random.choice([True, False, False])
    # 是否有市政消防栓
    has_hydrant = random.choice([True, False, False])
    # 距消防栓距离, m
    distance = 0
    # 市政消火栓的设计流量, L/s
    hydrant_flow = 15
    if no_outdoor:
        municipal_hydrant_flow_description += "市政给水管网能完全保证室外消防给水的用量"
    else:
        if has_hydrant:
            distance = random.choice([i * 5 for i in range(1, 13)])
        # 市政消火栓补水量, L/s
        if distance == 0:
            # 无市政消防栓
            hydrant_flow = 0
        elif distance > 40:
            # 市政消防栓距离过远
            hydrant_flow = 0
            municipal_hydrant_flow_description += "距该建筑物${}m$处有支状布置的市政消火栓{}套".format(distance, random.randint(2, 5))
        else:
            municipal_hydrant_flow_description += "距该建筑物${}m$处有支状布置的市政消火栓{}套".format(distance, random.randint(2, 5))
    return [no_outdoor, has_hydrant, distance, hydrant_flow, municipal_hydrant_flow_description]


def setAutoFireExtinguishingSystemFlow():
    """确定自动灭火系统水流量"""
    # 自动灭火系统
    auto_fire_extinguishing_systems = ["湿式自喷灭火系统", "干式自喷灭火系统", "水喷雾灭火系统", "泡沫灭火系统", "固定消防炮灭火系统", "雨淋系统"]
    # 选择 0 ~ 4 个系统
    chosen_systems = random.sample(auto_fire_extinguishing_systems, random.randint(0, 4))
    # 自动灭火系统流量设置为 20 ~ 40 L/s
    chosen_systems_flows = [random.choice([i * 5 for i in range(4, 9)]) for _ in range(len(chosen_systems))]
    # 取最大值
    max_auto_fire_extinguishing_system_flow = 0
    system_description = ""
    if len(chosen_systems) != 0:
        max_auto_fire_extinguishing_system_flow = max(chosen_systems_flows)
        system_description += "此外，建筑内还设置有全保护的自动灭火系统，其中"
        for chosen_system_index, chosen_system in enumerate(chosen_systems):
            system_description += "{}，设计流量为${}L/s$；".format(chosen_system, chosen_systems_flows[chosen_system_index])
    system_description = system_description.strip("；")
    return [chosen_systems, chosen_systems_flows, max_auto_fire_extinguishing_system_flow, system_description]


def setWaterCurtainFlow():
    """确定水幕系统水流量"""
    # 是否设置水幕系统
    has_water_curtain = random.choice([True, True, False])
    # 水幕系统水流量设置为 25 ~ 50 L/s
    water_curtain_flow = random.choice([i * 5 for i in range(5, 11)])
    water_curtain_description = ""
    water_curtain_usage = random.choice(["防火玻璃墙", "防火卷帘"])
    if has_water_curtain:
        water_curtain_description = "也设置有{}和冷却水幕，设计流量为${}L/s$".format(water_curtain_usage, water_curtain_flow)
    return [has_water_curtain, water_curtain_flow, water_curtain_usage, water_curtain_description]


def setIndoorHydrantFlowReduction(indoor_hydrant_flow, height, chosen_systems):
    """室内消防栓设计流量是否折减"""
    indoor_hydrant_flow_reduction = 0
    if (len(chosen_systems) > 0) and (0 < height <= 50) and (indoor_hydrant_flow > 20):
        indoor_hydrant_flow_reduction = 5
    return indoor_hydrant_flow_reduction


def setSupplyWaterFlow():
    """补水量"""
    # 消防给水路数
    supply_water_roads = random.choice([0, 1, 2])
    # 消防给水流量, 10 ~ 20 L/s
    supply_water_flows_range = [i * 5 for i in range(2, 5)]
    supply_water_flows = random.sample(supply_water_flows_range, supply_water_roads)
    supply_water_description = ""
    min_supply_water_flows = 0
    if supply_water_roads == 0:
        supply_water_description += "市政管网不提供额外的消防给水"
    elif supply_water_roads == 1:
        supply_water_description += "该建筑消防水池采用一路消防供水，在火灾情况下连续补水流量为${}L/s$".format(supply_water_flows[0])
    else:
        supply_water_description += "市政管网有符合要求的两条水管向水池补水，补水量分别为${}L/s$和${}L/s$".format(
            supply_water_flows[0], supply_water_flows[1]
        )
        min_supply_water_flows = min(supply_water_flows)
    return [supply_water_roads, supply_water_flows, min_supply_water_flows, supply_water_description]


def setWasteWaterQuestion(seed=None):
    """消防废水计算"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    # --- 1、确定题目已知量 --- #
    # 确定火灾持续时间
    duration, building_description, height = setDuration()
    # 确定室内外消防栓流量
    outdoor_hydrant_flow, indoor_hydrant_flow, hydrant_description = setHydrantFlow()
    # 确定室外市政消防栓流量
    no_outdoor, has_hydrant, distance, hydrant_flow, municipal_hydrant_flow_description = setMunicipalHydrantFlow()
    # 确定室外市政消防栓流量
    chosen_systems, chosen_systems_flows, max_auto_fire_extinguishing_system_flow, system_description = setAutoFireExtinguishingSystemFlow()
    # 确定水幕系统水流量
    has_water_curtain, water_curtain_flow, water_curtain_usage, water_curtain_description = setWaterCurtainFlow()
    # 确定室内消防栓设计流量是否折减
    indoor_hydrant_flow_reduction = setIndoorHydrantFlowReduction(indoor_hydrant_flow, height, chosen_systems)
    # 确定补水量
    supply_water_roads, supply_water_flows, min_supply_water_flows, supply_water_description = setSupplyWaterFlow()
    # --- 2、生成题目 --- #
    question = (building_description + "，")
    question += (hydrant_description + "。")
    if system_description:
        question += (system_description + "。")
    if water_curtain_description:
        question += (water_curtain_description + "。")
    if supply_water_description:
        question += (supply_water_description + "。")
    if municipal_hydrant_flow_description:
        question += (municipal_hydrant_flow_description + "。")
    if no_outdoor:
        question += "求该建筑消防水池最小有效容积。\n（考虑折减，计算中间数据以及最终结果均保留小数点后两位，单位为$m^3$）"
    else:
        question += "求该建筑消防水池最小有效容积和发生事故时在设计流量下的消防水量。\n（考虑折减，计算中间数据以及最终结果均保留小数点后两位，单位为$m^3$）"
    # --- 3、生成解析 --- #
    calculation_process = "解析："
    # --- 3.1、火灾持续时间 --- #
    calculation_process += "\n（1）首先查表确定火灾延续时间：\n$$\nt={}h\n$$".format(duration)
    # --- 3.2、室外消防栓用水量 --- #
    calculation_process += "\n（2）计算室外消防栓用水量$q_1$，"
    if no_outdoor:
        q_1 = 0
        q_o = 0
        calculation_process += "题目中已知，市政给水管网能完全保证室外消防给水的用量，所以室外消火栓用水量不计入水池容积：\n$$\nq_1={}\n$$".format(q_1)
    elif not has_hydrant:
        q_1 = round(3.6 * outdoor_hydrant_flow * duration, 2)
        calculation_process += "无室外市政消防栓：\n$$\nq_1=3.6\\times{}\\times{}={}m^3\n$$".format(outdoor_hydrant_flow, duration, q_1)
        q_o = 0
    else:
        if distance > 40:
            q_1 = round(3.6 * outdoor_hydrant_flow * duration, 2)
            calculation_process += "由于市政消防栓超过火源建筑$40m$，不能视为可靠补水，\n不参与计算，则：\n$$\nq_1=3.6\\times{}\\times{}={}m^3\n$$".format(
                outdoor_hydrant_flow, duration, q_1
            )
            q_o = 0
        else:
            q_o = round(3.6 * hydrant_flow * duration, 2)
            q_1_ = round(3.6 * outdoor_hydrant_flow * duration, 2)
            q_1 = q_1_ - q_o
            calculation_process += "延续时间内以室外消防栓设计流量算：\n$$\nq'_1=3.6\\times{}\\times{}={}m^3\n$$".format(
                outdoor_hydrant_flow, duration, q_1_
            )
            calculation_process += "\n由于市政消防栓处于距火源建筑$40m$范围内，是可靠补水，\n即室外市政消防栓补水量：\n$$\nq_o=3.6\\times{}\\times{}={}m^3\n$$".format(
                hydrant_flow, duration, q_o
            )
            calculation_process += "\n则：\n$$\nq_1=q'_1-q_o={}-{}={}m^3\n$$".format(
                q_1_, q_o, q_1
            )
    # --- 3.3、室内消防栓用水量 --- #
    calculation_process += "\n（3）计算室内消防栓用水量$q_2$，"
    if indoor_hydrant_flow_reduction > 0:
        q_2 = round(3.6 * (indoor_hydrant_flow - indoor_hydrant_flow_reduction) * duration, 2)
        calculation_process += "由于建筑内设有自动水灭火系统全保护，且为高度不超过$50m$的高层建筑，"
        calculation_process += "且室内消火栓系统设计流量为${}L/s>20L/s$，符合折减的情况，".format(indoor_hydrant_flow)
        calculation_process += "室内消火栓设计流量可减少$5L/s$，则：\n$$\nq_2=3.6\\times({}-{})\\times{}={}m^3\n$$".format(
            indoor_hydrant_flow, indoor_hydrant_flow_reduction, duration, q_2
        )
    else:
        q_2 = round(3.6 * indoor_hydrant_flow * duration, 2)
        calculation_process += "由题目可知，该建筑不符合折减的情况，则：\n$$\nq_2=3.6\\times{}\\times{}={}m^3\n$$".format(
            indoor_hydrant_flow, duration, q_2
        )
    # --- 3.4、自动喷水灭火系统用水量 --- #
    calculation_process += "\n（4）计算自动喷水灭火系统的用水量$q_3$，"
    if len(chosen_systems) == 0:
        q_3 = 0
        calculation_process += "由于该建筑不设有自喷系统，则：\n$$\nq_3={}\n$$".format(q_3)
    else:
        q_3 = round(3.6 * max_auto_fire_extinguishing_system_flow * 1, 2)
        calculation_process += "取自喷系统中最大的用水流量，且自喷系统用水时间为$1h$，则："
        calculation_process += "\n$$\nq_3=3.6\\times{}\\times1={}m^3\n$$".format(max_auto_fire_extinguishing_system_flow, q_3)
    # --- 3.5、水幕系统用水量 --- #
    calculation_process += "\n（5）计算水幕系统的用水量$q_4$，"
    if not has_water_curtain:
        q_4 = 0
        calculation_process += "由于该建筑不设有水幕系统，则：\n$$\nq_4={}\n$$".format(q_4)
    else:
        if water_curtain_usage == "防火卷帘":
            q_4 = round(3.6 * water_curtain_flow * 3, 2)
            calculation_process += "因水幕是对防火卷帘进行冷却，所以按$3.0h$：\n$$\nq_4=3.6\\times{}\\times3={}m^3\n$$".format(
                water_curtain_flow, q_4
            )
        else:
            q_4 = round(3.6 * water_curtain_flow * 1, 2)
            calculation_process += "因水幕是对防火玻璃墙进行冷却，所以按$1.0h$：\n$$\nq_4=3.6\\times{}\\times1={}m^3\n$$".format(
                water_curtain_flow, q_4
            )
    # --- 3.6、补水量 --- #
    calculation_process += "\n（6）计算补水量$q_5$，"
    if supply_water_roads == 0:
        q_5 = 0
        calculation_process += "由于市政管网不提供额外的消防给水，则：\n$$\nq_5={}\n$$".format(q_5)
    elif supply_water_roads == 1:
        q_5 = 0
        calculation_process += "由于补水管路为一路补水，补水不可靠，不考虑补水情况，则：\n$$\nq_5={}\n$$".format(q_5)
    else:
        q_5 = round(3.6 * min_supply_water_flows * duration, 2)
        calculation_process += "两路供水按最小者计入：\n$$\nq_5=3.6\\times{}\\times{}={}m^3\n$$".format(
            min_supply_water_flows, duration, q_5
        )
    q_w = round(q_1 + q_2 + q_3 + q_4 + q_o, 2)
    q_m = round(q_1 + q_2 + q_3 + q_4 - q_5, 2)
    # --- 3.7、消防水池最小有效容积 --- #
    calculation_process += "\n（7）消防水池最小有效容积：\n$$\nq_m=q_1+q_2+q_3+q_4-q_5\\\\={}+{}+{}+{}-{}={}m^3\n$$".format(
        q_1, q_2, q_3, q_4, q_5, q_m
    )
    if q_m <= 0:
        calculation_process += "\n也即该建筑理论上可不建设消防水池。"
    # --- 3.8、消防水量 --- #
    if not no_outdoor:
        if q_o == 0:
            calculation_process += "\n（8）消防水量：\n$$\nq_w=q_1+q_2+q_3+q_4\\\\={}+{}+{}+{}={}m^3\n$$".format(
                q_1, q_2, q_3, q_4, q_w
            )
        else:
            calculation_process += "\n（8）消防水量：\n$$\nq_w=q_1+q_2+q_3+q_4+q_o\\\\={}+{}+{}+{}+{}={}m^3\n$$".format(
                q_1, q_2, q_3, q_4, q_o, q_w
            )
    return question, calculation_process, q_m, q_w, no_outdoor
