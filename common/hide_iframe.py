# coding=utf8
"""
通用组件: 隐藏自定义的 iframe
"""
import streamlit as st

from conf.cdn import jquery


def hideIframe():
    """隐藏自定义的 JS 组件, 并显示 streamlit 原生组件"""
    code = """
        <head>
            <script type="text/javascript" src="%s"></script>
        </head>
        <body>
            <script>
                //先隐藏该组件
                window.frameElement.parentNode.style.display = "none";
                var elements = $(window.frameElement).parents().find("#root").find(".element-container");
                $.each(elements, function(index, element){
                    //无 iframe 的为原生组件组件
                    if ($(element).find("iframe").length == 0){
                        //无 stHidden 样式的需要显示
                        if ($(element).find(".stHidden").length == 0) {
                            $(element).show();
                        //否则也要隐藏
                        } else {
                            $(element).hide();
                        }
                    //有 iframe 的为自定义组件, 需要隐藏
                    } else {
                        $(element).hide();
                    }
                })
            </script>
        </body>
    """ % jquery
    st.components.v1.html(html=code, height=0)