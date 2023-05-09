# coding=utf8
"""
通用组件: 弹窗通知
"""
import time

import streamlit as st


def alertMsg(msg):
    """弹窗

    :param msg: 弹窗消息
    :return:
    """
    code = """
    <script>
        //隐藏该组件
        window.frameElement.parentNode.style.display="none";
        //弹窗提示
        alert(`%s`);
    </script>
    """ % msg
    st.components.v1.html(html=code, height=0)