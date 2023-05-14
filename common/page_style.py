# coding=utf8
"""
通用组件: 页面样式
"""
import streamlit as st

from conf.cdn import jquery, jquery_cookie, base64_min


def pageStyle():
    # 嵌入 js 脚本
    code = """
    <head>
        <script src="%s"></script>
        <script src="%s"></script>
        <script src="%s"></script>
    </head>
    <body>
        <script>
            //注销: 清除所有 cookie
            function clearAllCookie() {
                try {
                    if (confirm("确定注销吗？这将清除所有本地cookie并断开坚果云连接！") == true){ 
                        $.each($.cookie(), function(key, value){
                            try {
                                $.removeCookie(key, { path: "/" });
                                console.log("Remove-Cookie: " + key)
                            } catch(err) {
                                console.log(err)
                            }
                        })
                        alert("已注销！");
                        window.top.location.reload();
                    } else{ 
                        alert("已取消注销操作！");
                    }
                } catch(err) {
                    alert("清除 cookie 失败！");
                    console.log(err);
                }
            };
                
            //判断是电脑端还是手机端
            function isMobile() {
                var userAgentInfo = navigator.userAgent;
                var mobileAgents = ["Android", "iPhone", "SymbianOS", "Windows Phone", "iPad", "iPod"];
                var mobile_flag = false;
                //根据userAgent判断是否是手机
                for (var v = 0; v < mobileAgents.length; v++) {
                   if (userAgentInfo.indexOf(mobileAgents[v]) > 0) {
                         mobile_flag = true;
                         break;
                   }
                }
                return mobile_flag;
            }
            
            //主菜单增加几个按钮
            function addActionButton(color, id, text, href="javascript:void(0);", func="") {
                //如果存在这样的按钮则先删除
                if (root_document.find("#" + id).length > 0) {
                    root_document.find("#" + id).remove();
                }
                //创建一个节点
                var action_a = window.top.document.createElement("a");
                //设置颜色
                $(action_a).css("color", color);
                //去除下划线
                $(action_a).css("text-decoration", "none");
                //设置 id
                $(action_a).attr("id", id);
                //设置链接
                $(action_a).attr("href", href);
                //设置文本
                $(action_a).text(text)
                //绑定事件
                if (func != "") {
                    $(action_a).click(function(){func()});
                }
                //将按钮添加至主菜单
                MainMenu.before(action_a);
            }
            
            //先隐藏该组件
            window.frameElement.parentNode.style.display = "none";
            //获取根文档
            var root_document = $(window.frameElement).parents().find("#root");
            
            try {
                //进度条功能区删除
                var progress_box = $(window.frameElement).parents().find("#root").find("#progress-box");
                if (progress_box.length > 0) {
                    progress_box.remove();
                }
                //计时器删除
                var timer_box = $(window.frameElement).parents().find("#root").find("#timer-box");
                if (timer_box.length > 0) {
                    timer_box.remove();
                }
                //清除计时器
                var exam_timer = JSON.parse(Base64.decode($.cookie("exam_timer")));
                if (exam_timer.timer) {
                    window.top.clearInterval(exam_timer.timer);
                }
            } catch(err) {
                console.log(err)
            }
            
            //(1)修改底部说明为华工
            try {
                var footer = root_document.find("footer");
                footer.html("<p style='height:20px;line-height:20px;font-size=20px'><img src='https://www.scut.edu.cn/_upload/article/images/93/f1/da8bef494e929b2303b75fcae24a/76c44c1f-cc13-4b1c-b69c-1cb9e8e8aa3a.png' style='border-radius:50%%;height:20px'/>&nbsp;South China University of Technology</p>")
            } catch(err) {
                console.log(err)
            }
            
            //(2)修改页面边距, 只更改电脑端的
            if (isMobile() == false) {
                //然后边距调整
                footer.css("padding", "10px 0 10px 50px")
                //主页面边框减小
                root_document.find("section[tabindex=0]").find("div[class*='block-container']").css("padding", "50px");
                //侧边栏上边间隔减少
                root_document.find("div[data-testid='stSidebarNav']").find("ul").css("padding", "50px 0 16px 0"); 
            }
            
            //(3)页面顶部菜单增加几个按钮
            //获取主菜单
            var MainMenu = root_document.find("#MainMenu");
            //名字
            addActionButton("blue", "userinfo-action", "游客", href="./个人信息", func="");
            //坚果云连接状态
            addActionButton("orange", "jgy-action", "[云×]", href="./", func="");
            //注销按钮
            addActionButton("red", "exit-action", "[注销]", href="javascript:void(0);", func=clearAllCookie);
        </script>
    </body>
    """ % (jquery, jquery_cookie, base64_min)
    # 执行脚本
    st.components.v1.html(html=code, height=0)