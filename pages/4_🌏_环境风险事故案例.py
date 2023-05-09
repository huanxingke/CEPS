# coding=utf8
import json
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from common.init_user import initUserConfig
from common.hide_iframe import hideIframe
from conf.menu import menu_items
from conf.path import json_path
from core.query_cases import QueryCases
from core.case_card import caseCard


@st.cache_data()
def load_cases():
    with open(os.path.join(json_path, "cases.json"), "r", encoding="utf-8") as fp:
        cases_data = json.load(fp)
    return cases_data


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(page_title="环境风险事故案例", page_icon="🌏", layout="wide", menu_items=menu_items)
st.markdown("### 🌏 环境风险事故案例")
initUserConfig()
# ---------- End:每页基础配置 ---------- #

with st.spinner("正在载入案例数据..."):
    # 加载化学品数据
    cases = load_cases()
    # 加载搜索模型
    qc = QueryCases(cases=cases)

st.radio(
    "选择检索方式",
    ("关键词检索", "全部案例", "查看已标记"),
    horizontal=True,
    key="cases_query_mode",
    label_visibility="collapsed"
)
if st.session_state.get("cases_query_mode") == "全部案例":
    st.selectbox(
        "全部案例",
        [f"{i['index'] + 1}@ {i['name']}" for i in cases],
        key="cases_all_options",
        label_visibility="collapsed"
    )
    option_index = 0
    option = st.session_state.get("cases_all_options")
    if option:
        option_index = int(option.split("@")[0]) - 1
    caseCard(cases[option_index])
elif st.session_state.get("cases_query_mode") == "查看已标记":
    # 从应用会话中获取已标记案例
    marked_cases = st.session_state.get("marked_cases")
    if marked_cases:
        marked_cases_list = []
        for marked_cases_index in marked_cases:
            marked_cases_list.append(cases[marked_cases_index])
        st.selectbox(
            "已标记案例",
            [f"{i['index'] + 1}@ {i['name']}" for i in marked_cases_list],
            key="cases_marked_options",
            label_visibility="collapsed"
        )
        # 当前选择的选项
        option_index = 0
        option = st.session_state.get("cases_marked_options")
        if option:
            option_index = int(option.split("@")[0]) - 1
        caseCard(cases[option_index])
    else:
        st.warning("未标记任何案例！")
else:
    keywords = st.text_input(label="请输入要检索的案例关键词：", key="case_query_keywords")
    start_query = st.button("搜索", key="start_query_cases")
    # 点击搜索
    if start_query:
        with st.spinner("正在搜索..."):
            query_cases = qc.query(keywords=keywords)
            # 保存搜索结果于应用会话
            st.session_state.query_cases_index = [i["index"] for i in query_cases]
            if query_cases:
                st.selectbox(
                    "搜索结果如下",
                    [f"{i['index'] + 1}@ {i['name']}" for i in query_cases],
                    key="cases_query_options"
                )
                caseCard(query_cases[0])
            else:
                st.warning("无搜索结果！")
    # 此时如果再从多选框中选择, 会刷新 start_query 的状态
    # 因此调用应用会话中的数据, 这也是为什么保存 query_cases_index 于应用会话中
    elif st.session_state.get("cases_query_options"):
        # 从应用会话中提取搜索结果
        query_cases_index = st.session_state.get("query_cases_index")
        query_cases = []
        for query_case_index in query_cases_index:
            query_cases.append(cases[query_case_index])
        # 当前选择的选项
        option_index = 0
        option = st.session_state.get("cases_query_options")
        if option:
            option_index = int(option.split("@")[0]) - 1
        st.selectbox(
            "搜索结果如下",
            [f"{i['index'] + 1}@ {i['name']}" for i in query_cases],
            key="cases_query_options",
            index=query_cases.index(cases[option_index])
        )
        caseCard(cases[option_index])

# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件
hideIframe()
# ---------- End:每页基础配置 ---------- #