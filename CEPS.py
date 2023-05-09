# coding=utf8
"""
chemical-eps: Chemical Emergency Plan System
"""
import json

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from lib.Webdav import JianGuoYunClient
from common.init_user import initUserConfig
from common.action_button import addActionButton
from common.refresh import refreshPage
from common.hide_iframe import hideIframe
from conf.menu import menu_items


# 断开云盘链接
def disconnect(refresh=False):
    # 从应用会话中移除
    if st.session_state.get("jgy"):
        del st.session_state.jgy
    if st.session_state.get("user"):
        del st.session_state.user
    # 从本地 cookie 中移除
    JSCookieManager(key="user", delete=True)
    addActionButton(action_id="jgy-action", action_text="[云×]", action_color="orange", action_href="./")
    if refresh:
        # 刷新页面
        refreshPage()


# 展示云盘配置情况
def showUser():
    st.success("已成功连接至坚果云盘！")
    st.text_input(
        label="[坚果云]账户：", key="username",
        disabled=True, value=st.session_state.user.get("username")
    )
    st.text_input(
        label="[坚果云]应用密码：", key="password",
        disabled=True, type="password", value=st.session_state.user.get("password")
    )
    addActionButton(action_id="jgy-action", action_text="[云√]", action_color="green", action_href="./pageStyle.py")
    if st.button("断开连接", key="disconnect_login"):
        with st.spinner("正在断开连接..."):
            disconnect(refresh=True)


# ---------- Start:每页基础配置 ---------- #
st.set_page_config(page_title="首页", page_icon="🏠", layout="wide", menu_items=menu_items)
st.markdown("### 🏠 首页")
initUserConfig()
# ---------- End:每页基础配置 ---------- #

st.markdown("""
- 由于Streamlit暂无原生的持久化储存api，因此本程序采用 cookie + 坚果云的方式进行数据储存。
- 未连接云端时数据**只能保存于浏览器本地**。如需**云端储存**，请按以下教程开启[坚果云第三方应用授权**WebDAV**]：
- [坚果云第三方应用授权WebDAV开启方法](https://help.jianguoyun.com/?p=2064)
- 注：坚果云为目前国内最好用的支持webdav的云盘，且免费版每月有 1GB 上传和 3GB 下载流量，足够本系统进行数据云储存。
""")
# 从应用会话获取坚果云会话
jgy = st.session_state.get("jgy")
# 如果已连接坚果云, 直接显示坚果云配置
if jgy is not None:
    showUser()
# 如果未连接坚果云, 显示输入界面
else:
    st.text_input(label="输入账号：", key="username")
    st.text_input(label="输入应用密码：", key="password", type="password")
    st.button("确定", key="confirm_login")
    if st.session_state.confirm_login:
        username = st.session_state.username
        password = st.session_state.password
        # 尝试连接坚果云
        new_jgy = JianGuoYunClient(username=username, password=password)
        login_jgy = new_jgy.login()
        # 如果连接成功
        if login_jgy["code"] == 200:
            user = {
                "username": username,
                "password": password
            }
            # 保存坚果云配置于应用会话
            st.session_state.user = user
            # 保存坚果云会话于应用会话
            st.session_state.jgy = new_jgy
            # 保存坚果云配置于 cookie 中
            JSCookieManager(key="user", value=json.dumps(user))
            # 刷新页面
            refreshPage(alert="登录成功！点击刷新页面。")
        # 4.如果 -> 连接失败
        else:
            st.error("连接坚果云盘失败：{}".format(login_jgy["error"]))
            # 重置坚果云配置
            disconnect()

# ---------- Start:每页基础配置 ---------- #
# 隐藏自定义的 JS 组件
hideIframe()
# ---------- End:每页基础配置 ---------- #