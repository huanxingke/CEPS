# coding=utf8
"""
通用组件: 初始化页面数据
"""
from pathlib import Path
import base64
import json
import time
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from lib.CookieManager import CookieManager
from lib.Webdav import JianGuoYunClient
from common.alert import alertMsg
from common.action_button import addActionButton
from common.page_style import pageStyle


def initUserConfig():
    """初始化页面数据"""
    def autoLogin():
        """获取本地坚果云配置并尝试自动登录"""
        # 存在坚果云会话了就不必登录了
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            return
        # 必须获取到 cookie
        if (cookies is None) or (cookies.get("user") is None):
            return
        # 解析出坚果云配置
        user = json.loads(base64.b64decode(cookies.get("user")).decode())
        username = user["username"]
        password = user["password"]
        # 尝试连接云盘
        new_jgy = JianGuoYunClient(username=username, password=password)
        login_jgy = new_jgy.login()
        # 如果 -> 连接成功
        if login_jgy["code"] == 200:
            user = {
                "username": username,
                "password": password
            }
            # 保存坚果云配置于应用会话
            st.session_state.user = user
            # 保存坚果云会话于应用会话
            st.session_state.jgy = new_jgy
            return True
        return False

    def getUserData(param):
        """获取用户数据"""
        # 会话中已存在 param 跳过
        session_param = st.session_state.get(param)
        if session_param is not None:
            return
        # 首先从云端获取
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            cloud_param = jgy.get(param)
            # 如果获取成功
            if cloud_param and cloud_param.get("code") == 200:
                session_param = json.loads(base64.b64decode(cloud_param["value"]).decode())
                # 保存 param 于应用会话
                st.session_state[param] = session_param
                # 保存 param 于 cookie
                JSCookieManager(key=param, value=json.dumps(session_param))
        # 获取失败再从本地获取
        if session_param is None:
            # 必须获取到 cookie
            if cookies is not None and cookies.get(param) is not None:
                session_param = json.loads(base64.b64decode(cookies.get(param)).decode())
                # 保存 param 于应用会话
                st.session_state[param] = session_param
                # 如果已连接坚果云
                if jgy is not None:
                    # 保存 param 于云端
                    jgy.set(param=param, value=json.dumps(session_param))

    def uploadLearning():
        """上传学习进度"""
        # cookie 中有 current_learning 才执行
        if (cookies is None) or (cookies.get("current_learning") is None):
            return
        current_learning = json.loads(base64.b64decode(cookies.get("current_learning")).decode())
        learning_mode = current_learning["learning_mode"]
        knowledges_option = current_learning["knowledges_option"]
        # 保存于会话
        st.session_state.learning_mode = learning_mode
        st.session_state.knowledges_option = knowledges_option
        # 删除该 cookie
        JSCookieManager(key="current_learning", delete=True)
        # 必须有 jgy 和 learning_cookie 才上传
        jgy = st.session_state.get("jgy")
        if jgy is None:
            alertMsg(msg="未连接坚果云，上传学习进度失败！")
            return
        if cookies.get("learning_cookie") is None:
            alertMsg(msg="未找到学习记录！")
            return
        learning_cookie = json.loads(base64.b64decode(cookies.get("learning_cookie")).decode())
        # 上传云端
        upload_res = jgy.set(param="learning_cookie", value=json.dumps(learning_cookie))
        if upload_res.get("code") == 200:
            alertMsg(msg="已上传学习进度！")
        else:
            alertMsg(msg="学习进度上传失败！")

    def _actionButton_():
        """页面右上角显示"""
        # 姓名
        userinfo = st.session_state.get("userinfo")
        if userinfo is not None:
            show_name = userinfo["student_name"] if len(userinfo["student_name"]) <= 3 else f"{userinfo['student_name'][0]}*{userinfo['student_name'][-1]}"
            addActionButton(action_id="userinfo-action", action_text=show_name, action_href="./个人信息")
        # 坚果云连接状态
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            addActionButton(action_id="jgy-action", action_text="[云√]", action_color="green", action_href="./")

    def getExamTimer():
        """获取考试用时"""
        if (cookies is None) or (cookies.get("exam_timer") is None):
            return
        exam_timer = json.loads(base64.b64decode(cookies.get("exam_timer")).decode())
        st.session_state.exam_timer = exam_timer

    # ****** 网页基础样式更改 ****** #
    pageStyle()

    # ****** 获取本地所有 cookie ****** #
    cm = CookieManager()
    get_all = cm.getAll()
    cookies = None
    if get_all is not None:
        cookies = get_all.get("cookies")

    # ****** 自动获取配置 ****** #
    # 获取本地坚果云配置并尝试自动登录
    login_status = autoLogin()
    for i in range(2):
        if not login_status:
            login_status = autoLogin()
    # 获取用户个人信息
    getUserData(param="userinfo")
    # 获取标记的化学品
    getUserData(param="marked_chemicals")
    # 获取标记的案例
    getUserData(param="marked_cases")
    # 上传学习进度
    uploadLearning()
    # 获取学习进度
    getUserData(param="learning_cookie")
    # 获取考试用时
    getExamTimer()
    # 页面右上角显示
    _actionButton_()
