# coding=utf8
"""
落地浓度计算
"""
from calendar import monthrange
import datetime
import random
import math
import re


def last_day_of_month(date_value):
    """获取某月份的最后一天"""
    return date_value.replace(day=monthrange(date_value.year, date_value.month)[1]).day


def getTheta(year, month, day):
    """获取某日期的太阳倾角"""
    date = datetime.date(year, month, day)
    # 获取该日期是一年中的第几天
    day_num = int(date.strftime("%j"))
    delta_0 = 360 * day_num / 365
    delta_0_radians = math.radians(delta_0)
    delta_0_radians_2 = math.radians(delta_0 * 2)
    delta_0_radians_3 = math.radians(delta_0 * 3)
    # 太阳倾角
    theta = (0.006918 - 0.399912 * math.cos(delta_0_radians) + 0.070257 * math.sin(delta_0_radians) -
             0.006758 * math.cos(delta_0_radians_2) + 0.0009079 * math.sin(delta_0_radians_2) -
             0.002697 * math.cos(delta_0_radians_3) + 0.001480 * math.sin(delta_0_radians_3)) * 180 / math.pi
    theta = round(theta, 2)
    return day_num, theta


def getSunLevel(t_c, l_c, h_0):
    """获取太阳辐射等级

    :param t_c: 总云量, 1 ~ 10
    :param l_c: 低云量, l_c < t_c
    :param h_0: 太阳高度角
    :return:
    """
    level = 0
    if (t_c <= 4) and (l_c <= 4):
        if h_0 <= 15:
            level = -1
        elif 15 < h_0 <= 35:
            level = 1
        elif 35 < h_0 <= 65:
            level = 2
        elif h_0 > 65:
            level = 3
    elif (5 <= t_c < 7) and (l_c <= 4):
        if h_0 <= 15:
            level = 0
        elif 15 < h_0 <= 35:
            level = 1
        elif 35 < h_0 <= 65:
            level = 2
        elif h_0 > 65:
            level = 3
    elif (t_c >= 8) and (l_c <= 4):
        if h_0 <= 15:
            level = 0
        elif 15 < h_0 <= 35:
            level = 0
        elif 35 < h_0 <= 65:
            level = 1
        elif h_0 > 65:
            level = 1
    elif (t_c >= 7) and (5 <= l_c <= 7):
        if h_0 <= 15:
            level = 0
        elif 15 < h_0 <= 35:
            level = 0
        elif 35 < h_0 <= 65:
            level = 0
        elif h_0 > 65:
            level = 1
    else:
        if h_0 <= 15:
            level = 0
        elif 15 < h_0 <= 35:
            level = 0
        elif 35 < h_0 <= 65:
            level = 0
        elif h_0 > 65:
            level = 0
    return level


def getAirLevel(v_l, sun_level):
    """获取大气稳定度

    :param v_l: 地面风速
    :param sun_level: 太阳辐射等级
    :return:
    """
    level = ""
    if v_l <= 1.9:
        if sun_level == 3:
            level = "A～B"
        elif sun_level == 2:
            level = "A～B"
        elif sun_level == 1:
            level = "B"
        elif sun_level == 0:
            level = "D"
        elif sun_level == -1:
            level = "E"
        elif sun_level == -2:
            level = "F"
    elif 1.9 < v_l <= 2.9:
        if sun_level == 3:
            level = "B"
        elif sun_level == 2:
            level = "B"
        elif sun_level == 1:
            level = "C"
        elif sun_level == 0:
            level = "D"
        elif sun_level == -1:
            level = "E"
        elif sun_level == -2:
            level = "F"
    elif 2.9 < v_l <= 4.9:
        if sun_level == 3:
            level = "C"
        elif sun_level == 2:
            level = "B～C"
        elif sun_level == 1:
            level = "C"
        elif sun_level == 0:
            level = "D"
        elif sun_level == -1:
            level = "D"
        elif sun_level == -2:
            level = "E"
    elif 4.9 < v_l <= 5.9:
        if sun_level == 3:
            level = "C"
        elif sun_level == 2:
            level = "D"
        elif sun_level == 1:
            level = "D"
        elif sun_level == 0:
            level = "D"
        elif sun_level == -1:
            level = "D"
        elif sun_level == -2:
            level = "D"
    elif v_l > 5.9:
        if sun_level == 3:
            level = "C"
        elif sun_level == 2:
            level = "D"
        elif sun_level == 1:
            level = "D"
        elif sun_level == 0:
            level = "D"
        elif sun_level == -1:
            level = "D"
        elif sun_level == -2:
            level = "D"
    return level


def getM(air_level):
    """获取指数率速度计算中的常数 m

    :param air_level: 大气稳定度
    :return:
    """
    m = 0
    if air_level == "A":
        m = 0.1
    elif air_level == "B":
        m = 0.15
    elif air_level == "C":
        m = 0.20
    elif air_level == "D":
        m = 0.25
    else:
        m = 0.30
    return m


def getParams(air_level, x):
    """获取国标推荐的扩散参数

    :param air_level: 大气稳定度
    :param x: 下风距离/m
    :return:
    """
    gamma_1 = 0
    alpha_1 = 0
    gamma_2 = 0
    alpha_2 = 0
    if air_level == "A～B":
        air_level = "A"
    elif air_level == "D":
        air_level = "C～D"
    elif air_level == "E":
        air_level = "D～E"
    elif air_level == "F":
        air_level = "E"
    # 表 7-19 和表 7-20
    if air_level == "A":
        if x <= 1000:
            gamma_1 = 0.425809
            alpha_1 = 0.901074
        else:
            gamma_1 = 0.602052
            alpha_1 = 0.850934
        if x <= 300:
            alpha_2 = 1.12154
            gamma_2 = 0.0799904
        elif 300 < x <= 500:
            alpha_2 = 1.51360
            gamma_2 = 0.00854771
        else:
            alpha_2 = 2.10881
            gamma_2 = 0.000211545
    elif air_level == "B":
        if x <= 1000:
            gamma_1 = 0.281846
            alpha_1 = 0.914370
        else:
            gamma_1 = 0.396353
            alpha_1 = 0.865014
        if x <= 500:
            alpha_2 = 0.964435
            gamma_2 = 0.127190
        else:
            alpha_2 = 1.09356
            gamma_2 = 0.057025
    elif air_level == "B～C":
        if x <= 1000:
            gamma_1 = 0.229500
            alpha_1 = 0.919325
        else:
            gamma_1 = 0.314238
            alpha_1 = 0.875086
        if x <= 500:
            alpha_2 = 0.941015
            gamma_2 = 0.114682
        else:
            alpha_2 = 1.00770
            gamma_2 = 0.0757182
    elif air_level == "C":
        if x <= 1000:
            gamma_1 = 0.177157
            alpha_1 = 0.924279
        else:
            gamma_1 = 0.232123
            alpha_1 = 0.885157
        alpha_2 = 0.917595
        gamma_2 = 0.106803
    elif air_level == "C～D":
        if x <= 1000:
            gamma_1 = 0.143940
            alpha_1 = 0.926849
        else:
            gamma_1 = 0.189396
            alpha_1 = 0.886723
        if x <= 2000:
            alpha_2 = 0.838628
            gamma_2 = 0.126152
        elif 2000 < x <= 10000:
            alpha_2 = 0.756410
            gamma_2 = 0.235667
        else:
            alpha_2 = 0.815575
            gamma_2 = 0.136659
    elif air_level == "D":
        if x <= 1000:
            gamma_1 = 0.110726
            alpha_1 = 0.929418
        else:
            gamma_1 = 0.146669
            alpha_1 = 0.888723
        if x <= 1000:
            alpha_2 = 0.826212
            gamma_2 = 0.104634
        elif 1000 < x <= 10000:
            alpha_2 = 0.632023
            gamma_2 = 0.400167
        else:
            alpha_2 = 0.55536
            gamma_2 = 0.810763
    elif air_level == "D～E":
        if x <= 1000:
            gamma_1 = 0.0985631
            alpha_1 = 0.925118
        else:
            gamma_1 = 0.124308
            alpha_1 = 0.892794
        if x <= 2000:
            alpha_2 = 0.776864
            gamma_2 = 0.111771
        elif 2000 < x <= 10000:
            alpha_2 = 0.572347
            gamma_2 = 0.5289922
        else:
            alpha_2 = 0.499149
            gamma_2 = 1.03810
    elif air_level == "E":
        if x <= 1000:
            gamma_1 = 0.0864001
            alpha_1 = 0.920818
        else:
            gamma_1 = 0.101947
            alpha_1 = 0.896864
        if x <= 1000:
            alpha_2 = 0.788370
            gamma_2 = 0.0927529
        elif 1000 < x <= 10000:
            alpha_2 = 0.565188
            gamma_2 = 0.433384
        else:
            alpha_2 = 0.414743
            gamma_2 = 1.73241
    elif air_level == "F":
        if x <= 1000:
            gamma_1 = 0.0553634
            alpha_1 = 0.929418
        else:
            gamma_1 = 0.0733348
            alpha_1 = 0.888723
        if x <= 1000:
            alpha_2 = 0.784400
            gamma_2 = 0.0620765
        elif 1000 < x <= 10000:
            alpha_2 = 0.525969
            gamma_2 = 0.370015
        else:
            alpha_2 = 0.323659
            gamma_2 = 2.40691
    return gamma_1, alpha_1, gamma_2, alpha_2


def getParams2(air_level, sigma_z_max):
    """根据大气稳定度与最大铅直扩散参数反求所有扩散参数

    :param air_level: 大气稳定度
    :param sigma_z_max: 最大铅直扩散参数
    :return:
    """
    xs = []
    x_max_ls = []
    if air_level == "A":
        xs = [300, 500, 600]
    elif air_level == "B":
        xs = [500, 600]
    elif air_level == "B～C":
        xs = [500, 600]
    elif air_level == "C":
        xs = [500]
    elif air_level == "C～D":
        xs = [2000, 10000, 20000]
    elif air_level == "D":
        xs = [1000, 10000, 20000]
    elif air_level == "D～E":
        xs = [2000, 10000, 20000]
    elif air_level == "E":
        xs = [1000, 10000, 20000]
    elif air_level == "F":
        xs = [1000, 10000, 20000]
    for x in xs:
        _, _, gamma_2, alpha_2 = getParams(air_level=air_level, x=x)
        x_max = (sigma_z_max / gamma_2) ** (1 / alpha_2)
        _, _, gamma_21, alpha_21 = getParams(air_level=air_level, x=x_max)
        if (gamma_2 == gamma_21) and (alpha_2 == alpha_21):
            x_max_ls.append(x_max)
    return x_max_ls


def setPotency(seed=None):
    """落地浓度计算"""
    # 设置随机数种子
    if seed:
        random.seed(seed)
    # 经度(负西正东)
    longitude = random.choice(range(-180, 181))
    # 纬度(负南正北)(取靠近赤道的纬度值, 让太阳高度角尽可能大)
    latitude = random.choice(range(-45, 46))
    # 烟囱高度, m
    H_s = random.choice(range(50, 151))
    # 出口内径, m
    D = random.choice(range(1, 5))
    # 废气量, m3/h
    Q_v = random.choice(range(1, 10))
    # 倍率
    times_10 = random.choice(range(4, 6))
    # 烟气出口温度, ℃
    T_s = random.choice(range(90, 180))
    # 废气中某有害物质排放量, kg/h
    Q = random.choice(range(100, 601))
    # 环境大气温度, ℃
    T_a = random.choice(range(20, 39))
    # 总云量
    t_c = random.choice(range(1, 11))
    # 低云量
    if t_c <= 4:
        l_c = random.choice(range(1, t_c + 1))
    elif 5 <= t_c < 7:
        l_c = random.choice(range(1, 5))
    elif t_c >= 7:
        if t_c < 8:
            l_c = random.choice(range(5, 8))
        else:
            l_c = random.choice([random.choice(range(1, 5)), random.choice(range(8, t_c + 1))])
    # 地面风速, m/s
    v_l = round(random.choice([i * 0.1 for i in range(1, 100)]), 2)
    # 轴向距离, m
    x = random.choice([i * 10 for i in range(100, 601)])
    # 年份
    year = random.choice(range(1989, 2023))
    # 月份(北纬取春夏, 让太阳高度角尽可能大)
    if latitude >= 0:
        month = random.choice(range(3, 9))
    else:
        month = random.choice(list(range(1, 3)) + list(range(9, 13)))
    # 日期
    day = random.choice(range(1, last_day_of_month(datetime.datetime(year=year, month=month, day=1).date())))
    # 时间(取太阳高升的时间, 让太阳高度角尽可能大)
    hour = random.choice(range(9, 18))
    question = ""
    if longitude < 0:
        longitude = abs(longitude)
        question += f"在西经${longitude}°$、"
    else:
        question += f"在东经${longitude}°$、"
    if latitude < 0:
        latitude = abs(latitude)
        question += f"南纬${latitude}°$的某平原郊区，建有一个工厂。"
    else:
        question += f"在北纬${latitude}°$的某平原郊区，建有一个工厂。"
    question += f"工厂产生的含有某种有害物质$X$的废气是通过一座高${H_s}m$、出口内径为${D}m$的烟囱排放的。"
    question += f"废气量为${Q_v}×10^{times_10}m^3/h$（烟囱出口状态），烟气出口温度${T_s}℃$，有害物质$X$排放量为${Q}kg/h$。"
    question += f"在{year}年{month}月{day}日北京时间{hour}时，当地的气象状况是气温${T_a}℃$、云量${t_c}/{l_c}$、地面风速${v_l}m/s$，"
    question += f"试计算此时距烟囱${x}m$的轴向浓度和由该厂造成的有害物质$X$最大地面浓度及产生距离。"
    question += "（太阳倾角根据公式计算，烟气抬升公式和扩散参数采用国标推荐，浓度单位换算为$mg/m^3$，距离单位为$m$，计算结果均保留小数点后两位）"
    answer = "（1）确定已知量：\n"
    answer += f"- 经度：$\lambda={longitude}^o$\n"
    answer += f"- 纬度：$\\varphi={latitude}^o$\n"
    answer += f"- 烟囱实体高度：$H_s={H_s}m$\n"
    answer += f"- 烟囱出口直径：$D={D}m$\n"
    f_Q_v = round(Q_v * 10 ** times_10 / 3600, 2)
    answer += f"- 烟气（实际）排放量：$Q_v=Q_y={Q_v}\\times10^{times_10}m^3/h={f_Q_v}m^3/s$\n"
    f_T_s = round(T_s + 273.15, 2)
    answer += f"- 烟气出口温度：$T_s=273.15+{T_s}={f_T_s}K$\n"
    f_T_a = round(T_a + 273.15, 2)
    answer += f"- 环境大气温度：$T_s=273.15+{T_a}={f_T_a}K$\n"
    f_Q = round(Q * 10 ** 6 / 3600, 2)
    answer += f"- 源强：$Q={Q}kg/h={f_Q}mg/s$\n"
    answer += f"- 观测进行时的北京时间：$t={hour}h$\n"
    answer += f"- 水平扩散距离：$x={x}m$\n"
    answer += "\n（2）确定大气稳定度：\n"
    day_num, theta = getTheta(year=year, month=month, day=day)
    answer += f"- {year}年{month}月{day}日是这一年中的第{day_num}天，根据公式（1-8）计算得：$\\theta={theta}^o$\n"
    angle = 15 * hour + longitude - 300
    answer += f"- $15t+\lambda-300=15\\times{hour}+{longitude}-300={angle}(^o)$\n"
    h_0 = math.degrees(math.asin((math.sin(math.radians(latitude)) * math.sin(math.radians(theta)) + math.cos(math.radians(latitude)) * math.cos(math.radians(theta)) * math.cos(math.radians(angle)))))
    h_0 = abs(round(h_0, 2))
    answer += "- 将参数代入式（1-7）得太阳高度角：\n"
    answer += f"$$\nh_0=arcsin[sin{latitude}^osin({theta})^o+cos{latitude}^ocos({theta})^ocos({angle})^o]={h_0}^o\n$$\n"
    sun_level = getSunLevel(t_c=t_c, l_c=l_c, h_0=h_0)
    answer += f"- 根据云量${t_c}/{l_c}$和$h_0={h_0}^0$查表得太阳辐射等级为：${sun_level}$\n"
    air_level = getAirLevel(v_l=v_l, sun_level=sun_level)
    answer += f"- 由太阳辐射等级${sun_level}$和地面风速${v_l}m/s$查表得此时大气稳定度为：${air_level}类$\n"
    answer += "\n（3）确定确定烟囱口平均风速：\n"
    m = getM(air_level=air_level)
    answer += f"- 根据烟囱高度$z=H_s={H_s}m<=150m$以及稳定度{air_level}查表1-2确定风速指数：$m={m}$\n"
    answer += "- 高度$10m$处的风速近似为地面风速：$u_{10}=%sm/s$\n" % v_l
    answer += "- 代入式（1-2）得烟囱口处平均风速：\n"
    u_a = round(v_l * (H_s / 10) ** m, 2)
    answer += "$$\n\overline{u}=u_{10}\\bigg(\\frac{z}{10}\\bigg)^m=3{\\times}\\bigg(\\frac{%s}{10}\\bigg)^{%s}=%sm/s\n$$\n" % (H_s, m, u_a)
    answer += "\n（4）确定有效源高：\n"
    answer += "- 单位时间内排出烟气的热量，公式（2-3）：\n"
    Q_h = 0.35 * 101.325 * f_Q_v * (f_T_s - f_T_a) / f_T_s
    Q_h = round(Q_h, 2)
    answer += "$$\nQ_h=0.35p_aQ_v\\frac{T_s-T_a}{T_s}\\\\=0.35{\\times}101.325{\\times}%s{\\times}\\frac{%s-%s}{%s}=%skJ/s\n$$\n" % (
        f_Q_v, f_T_s, f_T_a, f_T_s, Q_h
    )
    answer += "- 烟气抬升公式采用国标推荐公式，由于：\n"
    if Q_h < 2090:
        answer += f"$$\nQ_h={Q_h}kJ/s<500\\times4.18=2090kJ/s\n$$\n"
        answer += "- 采用公式（2-4）进行计算：\n"
        delta_H = 2 * (1.5 * f_Q_v / (math.pi * (D ** 2) / 4) * D + 0.01 * Q_h) / u_a
        delta_H = round(delta_H, 2)
        answer += "$$\n\Delta{H}=\\frac{2(1.5{\\nu_s}D+0.01Q_{h})}{\overline{u}}\\\\=\\frac{2(1.5{\\frac{Q_v}{\pi{D}^2/4}}D+0.01Q_{h})}{\overline{u}}\\\\=\\frac{2{\\times}(1.5{\\times}{\\frac{%s}{\pi{\\times}{%s}^2/4}}{\\times}%s+0.01{\\times}%s)}{%s}=%sm\n$$\n" % (f_Q_v, D, D, Q_h, u_a, delta_H)
    else:
        answer += f"$$\nQ_h={Q_h}kJ/s>500\\times4.18=2090kJ/s\n$$\n"
        answer += "- 采用公式（2-2）进行计算：\n"
        if 2100 <= Q_h < 21000:
            n_0 = 0.332
            n_1 = round(3 / 5, 3)
            n_2 = round(2 / 5, 3)
        else:
            n_0 = 1.427
            n_1 = round(1 / 3, 3)
            n_2 = round(2 / 3, 3)
        answer += f"- 由平原郊区，查表2-1得：$n_0={n_0}, n_1={n_1}, n_2={n_2}$\n"
        delta_H = n_0 * (Q_h ** n_1) * (H_s ** n_2) * (u_a ** (-1))
        delta_H = round(delta_H, 2)
        answer += "$$\n\Delta{H}=n_0Q_h^{n_1}H_s^{n_2}{\overline{u}}^{-1}={%s}{\\times}{%s}^{%s}{\\times}{%s}^{%s}{\\times}{%s}^{-1}=%sm\n$$\n" % (
            n_0, Q_h, n_1, H_s, n_2, u_a, delta_H
        )
    H = round(H_s + delta_H, 2)
    answer += "- 根据式（2-1）算出有效源高：\n"
    answer += "$$\nH=H_s+\Delta{H}=%s+%s=%sm\n$$\n" % (H_s, delta_H, H)
    answer += "\n（5）确定轴线浓度：\n"
    answer += f"- 该工厂位于平原郊区，大气稳定度为{air_level}，"
    if air_level == "A～B":
        answer += "取稳定度相对更低的值A作为查表依据，"
    elif air_level == "D":
        answer += "向不稳定度方向提半级，即取稳定度为C～D作为查表依据，"
    elif air_level == "E":
        answer += "向不稳定度方向提半级，即取稳定度为D～E作为查表依据，"
    elif air_level == "F":
        answer += "向不稳定度方向提半级为E～F，再取稳定度相对更低的值E作为查表依据，"
    answer += f"又因为$x={x}m$，查表7-19和7-20得：\n"
    gamma_1, alpha_1, gamma_2, alpha_2 = getParams(air_level=air_level, x=x)
    answer += f"$$\n\gamma_1={gamma_1}, \\alpha_1={alpha_1}\\\\\gamma_2={gamma_2}, \\alpha_2={alpha_2}\n$$\n"
    sigma_y = round(gamma_1 * x ** alpha_1, 2)
    sigma_z = round(gamma_2 * x ** alpha_2, 2)
    answer += "- 代入扩散参数公式：\n"
    answer += "$$\n\sigma_y=%s\\times{%s}^{%s}=%s\\\\\sigma_z=%s\\times{%s}^{%s}=%s\n$$\n" % (
        gamma_1, x, alpha_1, sigma_y,
        gamma_2, x, alpha_2, sigma_z
    )
    answer += "- 根据高架连续点源地面轴线浓度公式（3-4）得：\n"
    rho_x = f_Q / (math.pi * u_a * sigma_y * sigma_z) * math.e ** (- H ** 2 / (2 * sigma_z ** 2))
    # x 处浓度太小, 需要重新出题
    if rho_x < 0.01:
        return setPotency(seed=seed * 1.1)
    rho_x = round(rho_x, 2)
    answer += "$$\n\\rho(%s,0,0,%s)=\\frac{Q}{\pi\overline{u}\sigma_y\sigma_z}exp\\bigg(-\\frac{H^2}{2\sigma_z^2}\\bigg)\\\\=\\frac{%s}{\pi{\\times}%s{\\times}%s{\\times}%s}exp\\bigg(-\\frac{%s^2}{2{\\times}%s^2}\\bigg)=%smg/m^3\n$$\n" % (
        x, H, f_Q, u_a, sigma_y, sigma_z, H, sigma_z, rho_x
    )
    answer += "\n（6）确定地面最大浓度及产生距离：\n"
    answer += "- 由式（3-6）求得出现最大地面浓度时的垂直扩散参数：\n"
    sigma_z_max = round(H / (2 ** 0.5), 2)
    answer += "$$\n\sigma_z\\big|_{x=x_{max}}=\\frac{H}{\sqrt{2}}=\\frac{%s}{\sqrt{2}}=%sm\n$$\n" % (H, sigma_z_max)
    x_max_ls = getParams2(air_level=air_level, sigma_z_max=sigma_z_max)
    # 没有符合要求的 x_max, 重新出题
    if len(x_max_ls) != 1:
        return setPotency(seed=seed * 1.1)
    x_max = round(x_max_ls[0], 2)
    gamma_1m, alpha_1m, gamma_2m, alpha_2m = getParams(air_level=air_level, x=x_max)
    answer += f"- 查表7-20，大气稳定度为{air_level}级时，根据不同的下风距离范围计算$x$并返回验算，最终可得：\n"
    answer += f"$$\n\gamma_1={gamma_1m}, \\alpha_1={alpha_1m}\\\\\gamma_2={gamma_2m}, \\alpha_2={alpha_2m}\n$$\n"
    answer += "- 求得最大浓度时轴向距离为：\n"
    answer += "$$\nx_{max}=\\bigg(\\frac{\sigma_z\\big|_{x=x_{max}}}{\gamma_2}\\bigg)^\\frac{1}{\\alpha_2}=\\bigg(\\frac{%s}{%s}\\bigg)^\\frac{1}{%s}=%sm\n$$\n" % (sigma_z_max, gamma_2m, alpha_2m, x_max)
    answer += "- 此时横向扩散参数：\n"
    sigma_y_max = round(gamma_1m * x_max ** alpha_1m, 2)
    answer += "$$\n\sigma_y=%s\\times{%s}^{%s}=%s\n$$\n" % (
        gamma_1m, x_max, alpha_1m, sigma_y_max
    )
    answer += "- 由式（3-5）求得地面最大浓度：\n"
    rho_max = 2 * f_Q * sigma_z_max / (math.pi * u_a * math.e * (H ** 2) * sigma_y_max)
    # x_max 处浓度太小, 需要重新出题
    if rho_max < 0.01:
        return setPotency(seed=seed * 1.1)
    rho_max = round(rho_max, 2)
    answer += "$$\n\\rho_{max}=\\frac{2Q}{\pi\overline{u}eH^2}\\frac{\sigma_z}{\sigma_y}=\\frac{2{\\times}%s}{\pi{\\times}%s{\\times}e{\\times}%s^2}{\\times}\\frac{%s}{%s}=%smg/m^3\n$$\n" % (
        f_Q, u_a, H, sigma_z_max, sigma_y_max, rho_max
    )
    return question, answer, rho_x, rho_max, x_max
