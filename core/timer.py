# coding=utf8
"""
核心组件: 计时器
"""
import time

import streamlit as st

from conf.cdn import jquery, jquery_cookie, base64_min


def timer():
    """开启计时器"""
    code = """
    <head>
        <script src="%s"></script>
        <script src="%s"></script>
        <script src="%s"></script>
    </head>
    <body>
        <script>
            function getTime(time) {
                // 转换为式分秒
                let h = parseInt(time / 60 / 60 %% 24)
                h = h < 10 ? '0' + h : h
                let m = parseInt(time / 60 %% 60)
                 m = m < 10 ? '0' + m : m
                let s = parseInt(time %% 60)
                 s = s < 10 ? '0' + s : s
                // 作为返回值返回
                return [h, m, s]
            }

            //先隐藏该组件
            window.frameElement.parentNode.style.display = "none";

            //如果已存在计时器, 先删除
            var timer_box = $(window.frameElement).parents().find("#root").find("#timer-box");
            if (timer_box.length > 0) {
                timer_box.remove();
            }
            //清除计时器
            var exam_timer = JSON.parse(Base64.decode($.cookie("exam_timer")));
            if (exam_timer.timer) {
                window.top.clearInterval(exam_timer.timer);
            }
            //计时器代码
            timer_box = '<div id="timer-box" style="width:255px;height:25px;margin-top:20px;">已用时间：<span id="timer">00:00:00</span></div>'
            //获取侧边栏
            var sidebar_container = $(window.frameElement).parents().find("#root").find("section[data-testid='stSidebar']").find("div[data-testid='stVerticalBlock']")[0];
            //将计时器加进侧边栏
            $(sidebar_container).after(timer_box);
            
            //计时
            var timer = window.top.setInterval(function(){
                try {
                    var exam_timer = JSON.parse(Base64.decode($.cookie("exam_timer")));
                    var res = getTime(exam_timer.used_time);
                    $(window.frameElement).parents().find("#root").find("#timer").text(`${res[0]}:${res[1]}:${res[2]}`);
                    exam_timer.used_time += 1;
                    exam_timer.timer = timer;
                    exam_timer.timestamp = (new Date()).getTime();
                    var cookie_string = Base64.encode(JSON.stringify(exam_timer));
                    $.cookie("exam_timer", cookie_string, { expires: 365, path: "/" });
                } catch {}
            }, 1000)
        </script>
    </body>
    """ % (jquery, jquery_cookie, base64_min)
    # 执行脚本
    st.components.v1.html(html=code, height=0)


def destroyTimer():
    """销毁计时器"""
    code = """
    <head>
        <script src="%s"></script>
        <script src="%s"></script>
        <script src="%s"></script>
    </head>
    <body>
        <script>
            //先隐藏该组件
            window.frameElement.parentNode.style.display = "none";

            //如果已存在计时器, 先删除
            var timer_box = $(window.frameElement).parents().find("#root").find("#timer-box");
            if (timer_box.length > 0) {
                timer_box.remove();
            }
            //清除计时器
            var exam_timer = JSON.parse(Base64.decode($.cookie("exam_timer")));
            if (exam_timer.timer) {
                window.top.clearInterval(exam_timer.timer);
            }
        </script>
    </body>
    """ % (jquery, jquery_cookie, base64_min)
    # 执行脚本
    st.components.v1.html(html=code, height=0)