# coding=utf8
"""
自建三方库: 获取 cookie (双向组件)
"""
import os

import streamlit.components.v1 as components
import streamlit as st


IS_RELEASE = True

if IS_RELEASE:
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    build_path = os.path.join(absolute_path, "frontend/build")
    _component_func = components.declare_component("cookie_manager", path=build_path)
else:
    _component_func = components.declare_component("cookie_manager", url="http://localhost:3000")


class CookieManager(object):
    def __init__(self):
        self.cookie_manager = _component_func

    def getAll(self):
        """获取所有 cookie

        :return: {"code": 200, "msg": "Success.", "cookies": cookies.getAll()}
        """
        response = self.cookie_manager(method="all", key="get_all")
        return response

