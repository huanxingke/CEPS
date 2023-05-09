# coding=utf8
import base64
import copy
import time
import json
import os

import streamlit as st

from common.init_user import initUserConfig
from common.hide_iframe import hideIframe
from conf.menu import menu_items
from core.set_plans import setPlans


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(
    page_title="应急演练模块", page_icon="🗒️", layout="wide", menu_items=menu_items, initial_sidebar_state="expanded"
)
initUserConfig()
# ---------- End:每页基础配置 ---------- #


def resetOptions():
    for options_title_i in options_titles:
        st.session_state[f"expand_{options_title_i}"] = False
        st.session_state[options_title_i] = []


with st.spinner("正在载入应急演练案例数据..."):
    # 加载应急演练案例数据
    themes, options_dict, plans = setPlans()

# 主题列表
themes_list = list(themes.keys())
# 选项题目
options_titles = ["former_periods", "command_centre", "engineering_team", "methods", "alert_team", "medical_team", "after_periods"]
options_titles_Ch = ["应急开始阶段", "指挥中心", "工程抢险组", "特殊情况处置", "警戒治安组", "医疗救护组", "应急结束阶段"]

# 主题对应的危化品
with st.sidebar:
    # 主题选择
    themes_option_index = 0
    if st.session_state.get("themes_option") is not None:
        themes_option_index = themes_list.index(st.session_state.get("themes_option"))
    themes_option = st.selectbox(
        "选择主题",
        themes_list,
        key="themes_option",
        index=themes_option_index,
        on_change=resetOptions
    )
    # 涉及的危化品
    chemical_types_list = themes[st.session_state.get("themes_option")]
    chemical_types_option_index = 0
    if st.session_state.get("chemical_types_option") in chemical_types_list:
        chemical_types_option_index = chemical_types_list.index(st.session_state.get("chemical_types_option"))
    chemical_types_option = st.selectbox(
        "选择涉及的危化品",
        chemical_types_list,
        key="chemical_types_option",
        index=chemical_types_option_index,
        on_change=resetOptions
    )


with st.form("plans"):
    for options_titles_index, options_title in enumerate(options_titles):
        st.multiselect(
            options_titles_Ch[options_titles_index],
            options_dict[options_title],
            default=st.session_state.get(options_title),
            key=options_title
        )
    if st.form_submit_button("预览演练步骤", use_container_width=True):
        step_index = 1
        for options_titles_index, options_title in enumerate(options_titles):
            if st.session_state.get(options_title):
                st.markdown(f":orange[{options_titles_Ch[options_titles_index]}]")
                for step in st.session_state[options_title]:
                    st.markdown(f":blue[\[{step_index}\]{step}]")
                    step_index += 1
        if step_index == 1:
            st.warning("您未选择任何演练步骤！")
    if st.form_submit_button("提交演练步骤", use_container_width=True):
        # 获取用户答案
        answers = {}
        for options_titles_index, options_title in enumerate(options_titles):
            answers[options_title] = st.session_state.get(options_title)
        # 获取正确答案
        for plan in plans:
            if plan["theme"] == st.session_state.get("themes_option"):
                if plan["chemical_types"] == st.session_state.get("chemical_types_option"):
                    correct_answers = plan
        # 展示正确答案
        step_index = 1
        # 评分细则
        report = ""
        # 总分
        grades = 0
        # 得分
        get_grades = 0
        for options_titles_index, options_title in enumerate(options_titles):
            report += f":orange[{options_titles_Ch[options_titles_index]}]\n\n"
            steps = answers[options_title]
            correct_steps = correct_answers[options_title]
            for step in correct_steps:
                # 交集, 即正确步骤
                if step in steps:
                    report += f"（+10）:green[\[{step_index}\]{step}]\n\n"
                    get_grades += 10
                # 未选择的步骤
                else:
                    report += f"（+0）:violet[\[{step_index}\]{step}]\n\n"
                step_index += 1
                grades += 10
            # 错误或多余的步骤
            left_steps = list(set(steps).difference(set(correct_steps)))
            for step in left_steps:
                report += f"（-5）:red[~~{step}~~]\n\n"
                get_grades -= 5
        # 百分制得分
        get_hundred_grades = round(get_grades * 100 / grades, 2)
        st.markdown(f"##### 演练总分：{grades}")
        st.markdown(f"##### 实际得分：{get_grades}")
        st.markdown(f"##### 百分制得分：{get_hundred_grades}")
        st.markdown(report)


# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件, 并显示 streamlit 原生组件
hideIframe()
# ---------- End:每页基础配置 ---------- #
