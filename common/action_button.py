# coding=utf8
"""
通用组件: 页面右上方按钮
"""
import streamlit as st

from conf.cdn import jquery


def addActionButton(action_id, action_text, action_href="javascript:void(0);", action_color="blue", action_func=""):
    # 嵌入 js 脚本
    code = """
    <head>
        <script src="%s"></script>
    </head>
    <body>
        <script>
            //先隐藏该组件
            window.frameElement.parentNode.style.display = "none";
            
            //获取根文档
            var root_document = $(window.frameElement).parents().find("#root");
            //主菜单
            var MainMenu = root_document.find("#MainMenu");
            //存在 id 为 action_id 的按钮了
            if (root_document.find("#%s").length > 0) {
                //获取该 id 为 action_id按钮
                var action_a = root_document.find("#%s");
                //更改样式, 颜色为 action_color
                $(action_a).attr("style", "color:%s;text-decoration:none");
                //更改按钮链接为 action_href
                $(action_a).attr("href", "%s");
                //更改按钮文本为 action_text
                $(action_a).text("%s");
            //不存在这样的按钮
            } else {
                //新建一个按钮
                var action_a = window.top.document.createElement("a");
                //设置样式, 颜色为 action_color
                $(action_a).attr("style", "color:%s;text-decoration:none");
                //设置 id 为 action_id
                $(action_a).attr("id", "%s");
                //设置链接为 action_href
                $(action_a).attr("href", "%s");
                //设置文本为 action_text
                $(action_a).text("%s")
                //绑定点击事件 action_func
                $(action_a).click(function(){%s});
                console.log("id: %s - click: %s");
                //添加至主菜单
                MainMenu.before(action_a);
            }
        </script>
    </body>
    """ % (jquery, action_id, action_id, action_color, action_href, action_text, action_color,
           action_id, action_href, action_text, action_func, action_id, action_func)
    # 执行脚本
    st.components.v1.html(html=code, height=0)