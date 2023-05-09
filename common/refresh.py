# coding=utf8
"""
通用组件: 刷新页面
"""
import time

import streamlit as st


def refreshPage(alert="null"):
    """刷新页面

    :param alert: 是否弹出提示框
    :return:
    """
    code = """
    <script>
        //隐藏该组件
        window.frameElement.parentNode.style.display="none";
        //弹窗提示
        if (`%s` != "null") {
            alert(`%s`);
        };
        //刷新整个页面
        window.top.location.reload()
    </script>
    """ % (alert, alert)
    if not alert:
        with st.spinner("即将刷新页面..."):
            waits = 0
            for i in range(2):
                time.sleep(1)
                waits += 1
            if waits >= 2:
                st.components.v1.html(html=code, height=0)
    else:
        st.components.v1.html(html=code, height=0)