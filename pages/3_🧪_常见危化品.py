# coding=utf8
import json
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from common.init_user import initUserConfig
from common.hide_iframe import hideIframe
from conf.menu import menu_items
from conf.path import json_path
from core.query_chemicals import QueryChemicals
from core.chemical_card import chemicalCard


@st.cache_data()
def load_chemicals():
    with open(os.path.join(json_path, "chemicals.json"), "r", encoding="utf-8") as fp:
        chemicals_data = json.load(fp)
    return chemicals_data


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(page_title="常见危险化学品", page_icon="🧪", layout="wide", menu_items=menu_items)
st.markdown("### 🧪 常见危险化学品")
initUserConfig()
# ---------- End:每页基础配置 ---------- #

with st.spinner("正在载入化学品数据..."):
    # 加载化学品数据
    chemicals = load_chemicals()
    # 加载搜索模型
    qc = QueryChemicals(chemicals=chemicals)

st.radio(
    "选择检索方式",
    ("关键词检索", "全部化学品", "查看已标记"),
    horizontal=True,
    key="chemicals_query_mode",
    label_visibility="collapsed"
)
if st.session_state.get("chemicals_query_mode") == "全部化学品":
    st.selectbox(
        "全部化学品",
        [f"{i['index'] + 1}@ {i['name'][0]}" for i in chemicals],
        key="chemicals_all_options",
        label_visibility="collapsed"
    )
    option_index = 0
    option = st.session_state.get("chemicals_all_options")
    if option:
        option_index = int(option.split("@")[0]) - 1
    chemicalCard(chemicals[option_index])
elif st.session_state.get("chemicals_query_mode") == "查看已标记":
    # 从应用会话中获取已标记化学品
    marked_chemicals = st.session_state.get("marked_chemicals")
    if marked_chemicals:
        marked_chemicals_list = []
        for marked_chemicals_index in marked_chemicals:
            marked_chemicals_list.append(chemicals[marked_chemicals_index])
        st.selectbox(
            "已标记化学品",
            [f"{i['index'] + 1}@ {i['name'][0]}" for i in marked_chemicals_list],
            key="chemicals_marked_options",
            label_visibility="collapsed"
        )
        # 当前选择的选项
        option_index = 0
        option = st.session_state.get("chemicals_marked_options")
        if option:
            option_index = int(option.split("@")[0]) - 1
        chemicalCard(chemicals[option_index])
    else:
        st.warning("未标记任何化学品！")
else:
    keywords = st.text_input(label="请输入要检索的化学品：", key="chemical_query_keywords")
    start_query = st.button("搜索", key="start_query_chemical")
    # 点击搜索
    if start_query:
        with st.spinner("正在搜索..."):
            # 如果是 CAS 号则精确查询
            if keywords.replace("-", "").isdigit():
                query_chemicals = [i for i in chemicals if keywords in i["cas_number"]]
            # 否则模糊匹配
            else:
                query_chemicals = qc.query(keywords=keywords)
            # 保存搜索结果于应用会话
            st.session_state.query_chemicals_index = [i["index"] for i in query_chemicals]
            if query_chemicals:
                st.selectbox(
                    f"【{keywords}】的搜索结果如下",
                    [f"{i['index'] + 1}@ {i['name'][0]}" for i in query_chemicals],
                    key="chemicals_query_options"
                )
                chemicalCard(query_chemicals[0])
            else:
                st.warning("无搜索结果！")
    # 此时如果再从多选框中选择, 会刷新 start_query 的状态
    # 因此调用应用会话中的数据, 这也是为什么保存 query_chemicals_index 于应用会话中
    elif st.session_state.get("chemicals_query_options"):
        # 从应用会话中提取搜索结果
        query_chemicals_index = st.session_state.get("query_chemicals_index")
        query_chemicals = []
        for query_chemical_index in query_chemicals_index:
            query_chemicals.append(chemicals[query_chemical_index])
        # 当前选择的选项
        option_index = 0
        option = st.session_state.get("chemicals_query_options")
        if option:
            option_index = int(option.split("@")[0]) - 1
        st.selectbox(
            f"【{keywords}】的搜索结果如下",
            [f"{i['index'] + 1}@ {i['name'][0]}" for i in query_chemicals],
            key="chemicals_query_options",
            index=query_chemicals.index(chemicals[option_index])
        )
        chemicalCard(chemicals[option_index])

# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件
hideIframe()
# ---------- End:每页基础配置 ---------- #
