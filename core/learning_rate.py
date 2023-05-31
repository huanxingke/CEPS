# coding=utf8
"""
核心组件: 学习进度记录
"""
import time

import streamlit as st

from conf.cdn import jquery, jquery_cookie, base64_min


def learningRate(chapter_index):
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
            //章节
            var chapter = "%s";
            //阅读模式
            var learning_mode = "%s";
            //获取学习进度 cookie
            var learning_cookie = $.cookie("learning_cookie");
            //不存在
            if (learning_cookie == undefined) {
                learning_cookie = {};
                learning_cookie[learning_mode] = {};
                learning_cookie[learning_mode][chapter] = 0;
            //存在
            } else {
                learning_cookie = JSON.parse(Base64.decode(learning_cookie));
                //阅读模式无记录
                if (learning_cookie[learning_mode] == undefined) {
                    learning_cookie[learning_mode] = {};
                }
                //阅读章节无记录
                if (learning_cookie[learning_mode][chapter] == undefined) {
                    learning_cookie[learning_mode][chapter] = 0;
                }
            }
            
            //进度条功能区
            //如果已存在进度条, 先删除
            var progress_box = $(window.frameElement).parents().find("#root").find("#progress-box");
            if (progress_box.length > 0) {
                progress_box.remove();
            }
            //进度条代码
            progress_div = '<div id="progress-box" style="display:grid;width:255px;height:42px;margin-top:20px;grid-template-rows:17px 5px 25px;"><div style="height:17px;display:flex;display:-webkit-flex;grid-row-start:1;grid-row-end:2;"><div style="width:202px;height:17px;border:1px solid #9e9e9e;border-radius:7.5px"><div style="width:0;height:15px;background:#325976;border-radius:7.5px" id="progress"></div></div><span style="margin-left:5px;width:48px;height:17px;line-height:17px;text-align:left" id="progress-text">0%%</span></div><div style="height:25px;display:flex;display:-webkit-flex;grid-row-start:3;grid-row-end:4;"><button id="clearLearningRate" style="height:25px;line-height:19px;border-radius:12.5px;width:90px;margin-left:0px;background:transparent;color:#9C9C9C">重置进度</button></div></div>'
            //获取侧边栏
            var sidebar_container = $(window.frameElement).parents().find("#root").find("section[data-testid='stSidebar']").find("div[data-testid='stVerticalBlock']")[0];
            //将进度条加进侧边栏
            $(sidebar_container).after(progress_div);
            
            //初始化进度条
            //获取页面
            var section = $(window.frameElement).parents().find("#root").find("section[tabindex=0]")[0];
            //移动到页面顶端
            $(section).scrollTop(0);
            //学习进度
            var learning_rate = parseInt(learning_cookie[learning_mode][chapter]);
            //进度条移到学习进度的位置
            $(window.frameElement).parents().find("#root").find("#progress").css("width", (2 * learning_rate).toString() + "px");
            if (learning_rate == 100) {
                $(window.frameElement).parents().find("#root").find("#progress-text").text("已完成");
            } else {
                $(window.frameElement).parents().find("#root").find("#progress-text").text(learning_rate + "%%");
            };
            //滚动条滚动事件
            $(section).scroll(function() {
                //现在的进度
                learning_rate_now = Math.round(100 * (this.scrollTop + this.clientHeight) / this.scrollHeight);
                //必须比已记录的进度大才进行记录
                if (learning_rate_now > learning_rate) {
                    learning_rate = learning_rate_now;
                    //进度条移动到现在的进度
                    $(window.frameElement).parents().find("#root").find("#progress").css("width", (2 * learning_rate).toString() + "px");
                    //进度条提示
                    if (learning_rate == 100) {
                        $(window.frameElement).parents().find("#root").find("#progress-text").text("已完成");
                    } else {
                        $(window.frameElement).parents().find("#root").find("#progress-text").text(learning_rate + "%%");
                    };
                    //记录此时的时间与进度
                    learning_cookie["timestamp"] = parseInt(new Date().getTime() / 1000);
                    learning_cookie[learning_mode][chapter] = learning_rate;
                    //写入 cookie
                    var cookie_string = Base64.encode(JSON.stringify(learning_cookie));
                    $.cookie("learning_cookie", cookie_string, { expires: 365, path: "/" });
                }
            });
            
            //重置按钮绑定事件
            $(window.frameElement).parents().find("#root").find("#clearLearningRate").click(function(){
                //重置学习进度
                learning_rate = 0;
                //移动到页面顶端
                $(section).scrollTop(0);
                //记录此时的时间与进度
                learning_cookie["timestamp"] = parseInt(new Date().getTime() / 1000);
                learning_cookie[learning_mode][chapter] = learning_rate;
                //写入 cookie
                var cookie_string = Base64.encode(JSON.stringify(learning_cookie));
                $.cookie("learning_cookie", cookie_string, { expires: 365, path: "/" });
            });
        </script>
    </body>
    """
    learning_mode = st.session_state.get("learning_mode")
    if learning_mode == "Markdown":
        learning_mode = "M"
    else:
        learning_mode = "P"
    code %= (jquery, jquery_cookie, base64_min, chapter_index, learning_mode)
    # 等待页面加载完成
    time.sleep(1)
    # 执行脚本
    st.components.v1.html(html=code, height=0)