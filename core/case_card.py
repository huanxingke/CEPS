# coding=utf8
"""
核心组件: 环境风险事故案例卡片
"""
import base64
import json
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager


def markedControl(case_index):
    """控制标记"""
    marked_cases = st.session_state.get("marked_cases")
    # 标记
    if st.session_state.get(f"marked-cases-{case_index}"):
        # 如果原来没有任何标记
        if marked_cases is None:
            # 初始化标记
            marked_cases = [case_index]
        # 如果已标记
        elif case_index not in marked_cases:
            # 添加标记
            marked_cases.append(case_index)
    else:
        # 如果已标记
        if (marked_cases is not None) and (case_index in marked_cases):
            # 剔除标记
            marked_cases.remove(case_index)
    # 更新会话
    st.session_state.marked_cases = marked_cases
    with st.spinner("正在保存标记"):
        # 如果已连接坚果云
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            # 保存标记于云端
            jgy.set(param="marked_cases", value=json.dumps(marked_cases))
        # 保存标记于 cookie
        JSCookieManager(key="marked_cases", value=json.dumps(marked_cases))


def caseCard(case):
    """案例卡片"""
    # 品名与分类
    name = case["name"]
    # 标题
    st.markdown(f"<h4>{name}</h4>", unsafe_allow_html=True)
    # 是否标记该案例
    case_index = case["index"]
    marked_cases = st.session_state.get("marked_cases")
    if (marked_cases is not None) and (case_index in marked_cases):
        st.checkbox("标记", key=f"marked-cases-{case_index}", value=True, on_change=lambda: markedControl(case_index))
    else:
        st.checkbox("标记", key=f"marked-cases-{case_index}", value=False, on_change=lambda: markedControl(case_index))
    # 导航栏
    tab1, tab2, tab3, tab4 = st.tabs(["基础信息", "应急响应措施", "应急管理评价", "现场处置评价"])
    # 基础信息
    with tab1:
        # 时间
        when = case["when"]
        st.markdown(f" **时间：** {when}")
        # 地点
        where = case["where"]
        st.markdown(f" **地点：** {where}")
        # 主体
        who = case["who"]
        st.markdown(f" **主体：** {who}")
        # 事件
        event = case["event"]
        st.markdown(f" **事件：** {event}")
        # 关键词
        keywords = case["keywords"].replace("\n", "")
        st.markdown(f" **关键词：** {keywords}")
    # 应急响应措施
    with tab2:
        emergency_response = case["emergency_response"].split("\n")
        for i in emergency_response:
            st.write(i)
    # 应急管理评价
    with tab3:
        emergency_management_evaluation = case["emergency_management_evaluation"].split("\n")
        for i in emergency_management_evaluation:
            st.write(i)
    # 现场处置评价
    with tab4:
        onsite_disposal_evaluation = case["onsite_disposal_evaluation"].split("\n")
        for i in onsite_disposal_evaluation:
            st.write(i)