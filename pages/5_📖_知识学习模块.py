# coding=utf8
import base64
import json
import time
import os
import re

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from common.init_user import initUserConfig
from common.refresh import refreshPage
from common.hide_iframe import hideIframe
from conf.menu import menu_items
from conf.path import pdf_path, md_path, images_learning_path, images_knowledge_path
from core.learning_rate import learningRate


def dataFile():
    with open(os.path.join(pdf_path, "{}.pdf".format(st.session_state.get("knowledges_option"))), "rb") as pdf:
        return pdf.read()


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(
    page_title="知识学习模块", page_icon="📖", layout="wide", menu_items=menu_items, initial_sidebar_state="expanded"
)
initUserConfig()
# ---------- End:每页基础配置 ---------- #

knowledges = [
    i.replace(".md", "") for i in sorted(os.listdir(md_path))
]
modes = ["Markdown", "图片"]
with st.sidebar:
    # 章节选择
    knowledges_option_index = 0
    if st.session_state.get("knowledges_option") is not None:
        knowledges_option_index = knowledges.index(st.session_state.get("knowledges_option"))
    knowledges_option = st.selectbox(
        "选择章节",
        knowledges,
        key="knowledges_option",
        index=knowledges_option_index
    )
    # 阅读模式选择
    learning_mode_index = 0
    if st.session_state.get("learning_mode") is not None:
        learning_mode_index = modes.index(st.session_state.get("learning_mode"))
    st.radio(
        "切换阅读方式",
        modes,
        horizontal=True,
        key="learning_mode",
        index=learning_mode_index
    )
    st.markdown("由于Streamlit对Markdown格式支持有限，如有格式错乱可下载PDF后再阅读学习。")
    col1, col2 = st.columns(2)
    with col1:
        # 下载 PDF 文件
        st.download_button(
            label="下载PDF",
            data=dataFile(),
            file_name="{}.pdf".format(st.session_state.get("knowledges_option")),
            mime="application/octet-stream",
        )
    with col2:
        # 上传学习进度
        if st.button("上传进度", key="upload_leaning"):
            # 保存当前学习章节于 cookie
            current_learning = {
                "learning_mode": st.session_state.get("learning_mode"),
                "knowledges_option": st.session_state.get("knowledges_option")
            }
            JSCookieManager(key="current_learning", value=json.dumps(current_learning))
            refreshPage(alert="点此刷新页面以上传学习进度。")
with st.spinner("加载页面"):
    # 以 markdown 方式阅读
    if st.session_state.get("learning_mode") == "Markdown":
        with open(
                os.path.join(md_path, "{}.md".format(st.session_state.get("knowledges_option"))),
                "r", encoding="utf-8"
        ) as fp:
            # 这里增加表格与表格间的间距
            knowledge = fp.read().replace("</table>", "</table><br/>")
            # 图片路径
            img_path = os.path.join(images_knowledge_path, "{}.png")
            # 匹配 md 里的图片链接
            pattern = re.compile(r"!\[(.*?)\]\((.*?)\)")
            # 第一项为图片名, 第二项为链接
            for img_name, img_src in pattern.findall(knowledge):
                # 先还原原文的链接
                img_link = "![{}]({})".format(img_name, img_src)
                # 从本地获取图片
                with open(img_path.format(img_name), "rb") as img:
                    # 然后转换为 base64 链接
                    img_src = f"data:image/png;base64,{base64.b64encode(img.read()).decode()}"
                # 组合成新的链接
                new_img_link = "<img style='width:60%' src='{}' alt='{}'/>".format(img_src, img_name)  # "![{}]({})".format(img_name, img_src)
                # 替换掉原来的链接
                knowledge = knowledge.replace(img_link, new_img_link)
            st.markdown(knowledge, unsafe_allow_html=True)
            learningRate(chapter_index=knowledges.index(st.session_state.get("knowledges_option")))
    # 以图片方式阅读
    else:
        knowledges_pics_path = os.path.join(images_learning_path, st.session_state.get("knowledges_option"))
        knowledges_pics = sorted(os.listdir(knowledges_pics_path))
        for knowledges_pic in knowledges_pics:
            with open(os.path.join(knowledges_pics_path, knowledges_pic), "rb") as img:
                st.image(img.read())
        learningRate(chapter_index=knowledges.index(st.session_state.get("knowledges_option")))

# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件, 并显示 streamlit 原生组件
hideIframe()
# ---------- End:每页基础配置 ---------- #