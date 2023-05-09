# coding=utf8
"""
自建三方库: 获取 cookie (单向组件)
"""
import base64
import json
import re

import streamlit as st

from conf.cdn import jquery, jquery_cookie


def JSCookieManager(key="", value="", delete=False, nobase64=False):
    """控制 JS 端的 cookie

    :param key: cookie 键
    :param value: cookie 值
    :param delete: 是否是删除操作
    :param nobase64: 是否不需要 base64
    :return:
    """
    if delete:
        if key:
            # 删除指定 cookie
            code = """
            <head>
                <script type="text/javascript" src="%s"></script>
                <script type="text/javascript" src="%s"></script>
            </head>
            <body>
                <script>
                    //先隐藏该组件
                    window.frameElement.parentNode.style.display = "none";
                    //删除 cookie
                    try {
                        $.removeCookie(`%s`, { path: "/" });
                        console.log("Remove-Cookie: %s")
                    } catch(err) {
                        console.log(err)
                    }
                </script>
            </body>
            """ % (jquery, jquery_cookie, key, key)
        else:
            # 删除所有 cookie
            code = """
            <head>
                <script type="text/javascript" src="%s"></script>
                <script type="text/javascript" src="%s"></script>
            </head>
            <body>
                <script>
                    //先隐藏该组件
                    window.frameElement.parentNode.style.display = "none";
                    //删除所有 cookie
                    $.each($.cookie(), function(key, value){
                        try {
                            $.removeCookie(key, { path: "/" });
                            console.log("Remove-Cookie: " + key)
                        } catch(err) {
                            console.log(err)
                        }
                    })
                </script>
            </body>
            """ % (jquery, jquery_cookie)
    else:
        # 以 base64 储存
        if not nobase64:
            value = base64.b64encode(str(value).encode()).decode()
        # 储存 cookie
        code = """
        <head>
            <script type="text/javascript" src="%s"></script>
            <script type="text/javascript" src="%s"></script>
        </head>
        <body>
            <script>
                //先隐藏该组件
                window.frameElement.parentNode.style.display = "none";
                //设置 cookie
                try {
                    $.cookie(`%s`, `%s`, { expires: 365, path: "/" });
                    console.log("Set-Cookie: %s=%s")
                } catch(err) {
                    console.log(err)
                }
            </script>
        </body>
        """ % (jquery, jquery_cookie, key, value, key, value)
    st.components.v1.html(html=code, height=0)