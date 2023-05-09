# coding=utf8
import os

import streamlit as st

from common.init_user import initUserConfig
from common.hide_iframe import hideIframe
from conf.path import root_path, images_common_path
from conf.menu import menu_items


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(page_title="关于", page_icon="❔", layout="wide", menu_items=menu_items)
st.markdown("### ❔ 关于")
initUserConfig()
# ---------- End:每页基础配置 ---------- #

# 加载 README.md
with st.spinner("正在加载本站信息..."):
    with open(os.path.join(root_path, "README.md"), "r", encoding="utf-8") as fp:
        st.markdown(fp.read())
    with open(os.path.join(images_common_path, "motto.jpg"), "rb") as fp:
        st.image(fp.read())

# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件
hideIframe()
# ---------- End:每页基础配置 ---------- #