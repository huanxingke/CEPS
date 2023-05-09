# coding=utf8
"""
核心组件: 化学品卡片
"""
import base64
import json
import os

import streamlit as st

from lib.JSCookieManager import JSCookieManager
from conf.path import images_struct_path, images_ghs_path


# 类别颜色
category_colors = {
    "严重眼损伤/眼刺激": "#FF8C69",
    "加压气体": "#836FFF",
    "危害水生环境-急性危害": "#6B8E23",
    "危害水生环境-长期危害": "#BDB76B",
    "危害臭氧层": "#008B8B",
    "急性毒性-吸入": "#FFA500",
    "急性毒性-经口": "#EE9A00",
    "急性毒性-经皮": "#CD8500",
    "无分类": "#D3D3D3",
    "易燃固体": "#696969",
    "易燃气体": "#00BFFF",
    "易燃液体": "#1E90FF",
    "有机过氧化物": "#FF69B4",
    "氧化性固体": "#6A5ACD",
    "氧化性气体": "#8470FF",
    "氧化性液体": "#7B68EE",
    "爆炸物": "#A52A2A",
    "特异性靶器官毒性-一次接触": "#FFAEB9",
    "特异性靶器官毒性-反复接触": "#EEA2AD",
    "生殖毒性": "#8B4513",
    "生殖细胞致突变性": "#AB82FF",
    "皮肤腐蚀/刺激": "#FFA54F",
    "皮肤致敏物": "#EE9A49",
    "自反应物质和混合物": "#8B8970",
    "自热物质和混合物": "#C1CDC1",
    "自燃固体": "	#68838B",
    "自燃液体": "#9AC0CD",
    "致癌性": "#FF0000",
    "遇水放出易燃气体的物质和混合物": "#8B4513",
    "金属腐蚀物": "#838B8B"
}
# 象形图含义
GHS_meanings = {
    "GHS01": "1、符号名称：引爆的炸弹。\n2、代表化学品或危害：\n（1）爆炸物；\n（2）自反应物质和混合物；\n（3）有机过氧化物，其受热时可能引起爆炸。",
    "GHS02": "1、符号名称：火焰。\n2、代表化学品或危害：\n（1）极易燃气体；\n（2）发火气体；\n（3）化学不稳定气体；\n（4）极易燃气溶胶；\n（5）加压化学品；\n（6）易燃液体；\n（7）易燃固体；\n（8）自反应物质和混合物；\n（9）发火液体和发火固体；\n（10）自热物质和混合物；\n（11）遇水释放出易燃气体的物质和混合物；\n（12）有机过氧化物；\n（13）退敏爆炸物。",
    "GHS03": "1、符号名称：火焰包围圆环。\n2、代表化学品或危害：\n（1）氧化性气体；\n（2）氧化性固体；\n（3）氧化性液体。其受热时可能引起爆炸。\n3、这些化学品可能引燃或者加剧燃烧和爆炸。",
    "GHS04": "1、符号名称：气体钢瓶。\n2、代表化学品或危害：\n（1）加压化学品：受热可能爆炸；\n（2）内装加压气体；受热可能爆炸\n（3）内装冷冻气体，可能造成低温灼伤或损伤；\n（4）溶解气体。",
    "GHS05": "1、符号名称：腐蚀。\n2、代表化学品或危害：\n（1）腐蚀性的，且可能造成皮肤烧伤和严重眼睛损伤；\n（2）金属腐蚀物。",
    "GHS06": "1、符号名称：骷髅旗。\n2、代表化学品或危害：具有剧烈毒性或高急性毒性，与皮肤接触、吸入或者吞咽致命或有毒。",
    "GHS07": "1、符号名称：感叹号。\n2、代表化学品或危害：\n（1）急性毒性（有害的）；\n（2）引起皮肤过敏；\n（3）皮肤刺激或眼睛严重刺激；\n（4）呼吸道刺激；\n（5）麻醉性，引起嗜睡或眩晕；\n（6）破坏臭氧层，危害公众健康和环境。",
    "GHS08": "1、符号名称：健康危害。\n2、代表化学品或危害：\n（1）致癌性；\n（2）可能损害生育能力和未出生胎儿有影响；\n（3）致突变性；\n（4）呼吸过敏，吸入可能引起过敏、哮喘或呼吸困难；\n（5）特定靶器官毒性；\n（6）吸入危害；\n（7）如果吞咽或进入呼吸道，可能致命或有害。",
    "GHS09": "1、符号名称：环境。\n2、代表化学品或危害：危害环境，对水生生物毒性非常大或有毒，且具有长期持续影响。",
}


def markedControl(chemical_index):
    """控制标记"""
    marked_chemicals = st.session_state.get("marked_chemicals")
    # 标记
    if st.session_state.get(f"marked-{chemical_index}"):
        # 如果原来没有任何标记
        if marked_chemicals is None:
            # 初始化标记
            marked_chemicals = [chemical_index]
        # 如果已标记
        elif chemical_index not in marked_chemicals:
            # 添加标记
            marked_chemicals.append(chemical_index)
    else:
        # 如果已标记
        if (marked_chemicals is not None) and (chemical_index in marked_chemicals):
            # 剔除标记
            marked_chemicals.remove(chemical_index)
    # 更新会话
    st.session_state.marked_chemicals = marked_chemicals
    with st.spinner("正在保存标记"):
        # 如果已连接坚果云
        jgy = st.session_state.get("jgy")
        if jgy is not None:
            # 保存标记于云端
            jgy.set(param="marked_chemicals", value=json.dumps(marked_chemicals))
        # 保存标记于 cookie
        JSCookieManager(key="marked_chemicals", value=json.dumps(marked_chemicals))


def chemicalCard(chemical):
    """化学品卡片"""
    # 品名与分类
    name = chemical["name"][0]
    category = chemical["category"]
    category_color = category_colors[category]
    # 标题
    st.markdown(f"<h4>{name}&nbsp;<sup style='color:{category_color}'>{category}</sup></h4>", unsafe_allow_html=True)
    # 是否标记该化学品
    chemical_index = chemical["index"]
    marked_chemicals = st.session_state.get("marked_chemicals")
    if (marked_chemicals is not None) and (chemical_index in marked_chemicals):
        st.checkbox("标记", key=f"marked-{chemical_index}", value=True, on_change=lambda: markedControl(chemical_index))
    else:
        st.checkbox("标记", key=f"marked-{chemical_index}", value=False, on_change=lambda: markedControl(chemical_index))
    # 导航栏
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["基础信息", "理化特性", "CAS", "GHS", "危害与应急"])
    # 基础信息
    with tab1:
        # 别名
        if len(chemical["name"]) > 1:
            names = "；".join(chemical["name"][1:])
        else:
            names = "/"
        st.markdown(f" **别名：** {names}")
        # 英文名
        ename = "；".join(chemical["enName"])
        st.markdown(f" **英文名：** {ename}")
        # 临界量
        critical_quantity = chemical["critical_quantity"]
        if critical_quantity:
            st.markdown(f" **储存临界量：** {critical_quantity}t")
        # 危险性类别
        weixianxingleibie = ""
        for risk_type in chemical["weixianxingleibie"]:
            weixianxingleibie += f" - {risk_type}\n"
        st.markdown(" **危险性类别：**")
        st.markdown(weixianxingleibie)
    # 理化特性
    with tab2:
        # 理化特性
        lihuatexing = "<table><tbody>"
        for physicochemical_property in chemical["lihuatexing"]:
            property_name = physicochemical_property["name"]
            property_value = physicochemical_property["property"]
            lihuatexing += f"<tr><th>{property_name}</th><td>{property_value}</td></tr>"
        lihuatexing += "</tbody></table>"
        st.markdown(lihuatexing, unsafe_allow_html=True)
    # CAS 与结构式
    with tab3:
        cas_number_list = chemical["cas_number"]
        st.selectbox(
            "化学品 CAS 号",
            cas_number_list,
            key="cas_number_option",
            label_visibility="collapsed"
        )
        cas_number = st.session_state.cas_number_option
        molecular_formula = chemical["molecular_formula"][cas_number_list.index(cas_number)]
        st.markdown(" **分子式：** " + molecular_formula, unsafe_allow_html=True)
        # 结构式图片路径
        struct_pic_path = os.path.join(images_struct_path, "{}.jpg")
        # 结构式图片展示
        struct_pic = ""
        if os.path.exists(struct_pic_path.format(cas_number)):
            with open(struct_pic_path.format(cas_number), "rb") as fp:
                # 转化为 base64
                struct_pic = "data:image/png;base64," + base64.b64encode(fp.read()).decode()
        if struct_pic:
            st.image(struct_pic, width=150)
        else:
            st.text("结构式图片未收录！")
    # GHS 象形图展示
    with tab4:
        ghs_list = chemical["xiangxingtu"]
        for ghs in ghs_list:
            ghs_pic = os.path.join(images_ghs_path, f"{ghs}.gif")
            with open(ghs_pic, "rb") as fp:
                # 转化为 base64
                ghs_pic_b64 = "data:image/png;base64," + base64.b64encode(fp.read()).decode()
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(GHS_meanings[ghs].replace("\n", "<br/>"), unsafe_allow_html=True)
            with col2:
                st.image(ghs_pic_b64, width=100)
            st.divider()
    # 危害与应急
    with tab5:
        # 主要用途
        zhuyaoyongtu = chemical["zhuyaoyongtu"]
        st.markdown(f" **主要用途：** {zhuyaoyongtu}")
        # 环境危害
        huanjingweihai = chemical["huanjingweihai"]
        st.markdown(f" **环境危害：** {huanjingweihai}")
        # 燃烧与爆炸危险性
        ranshaoyubaozhaweixianxing = chemical["ranshaoyubaozhaweixianxing"]
        # 化学活性
        huoxingfanying = chemical["huoxingfanying"]
        st.markdown(
            f" **化学活性：**\n"
            f" - **爆燃特性**：{ranshaoyubaozhaweixianxing}\n"
            f" - **活性反应**：{huoxingfanying}"
        )
        # 毒性
        duxing = chemical["duxing"]
        # 中毒表现
        zhongdubiaoxian = chemical["zhongdubiaoxian"]
        st.markdown(
            f" **毒性：**\n"
            f" - **毒性实验**：{duxing}\n"
            f" - **中毒表现**：{zhongdubiaoxian}"
        )
        # 急救措施
        jijiucuoshi = chemical["jijiucuoshi"]
        jijiucuoshi_string = ""
        for jijiucuoshi_i in jijiucuoshi.split(";"):
            jijiucuoshi_i = jijiucuoshi_i.replace(":", "：").strip()
            if jijiucuoshi_i:
                jijiucuoshi_i_list = jijiucuoshi_i.split("：")
                if len(jijiucuoshi_i_list) == 1:
                    jijiu_i_type, jijiu_i_method = jijiucuoshi_i_list[0], "无资料。"
                else:
                    jijiu_i_type, jijiu_i_method = jijiucuoshi_i_list[0], jijiucuoshi_i_list[1]
                jijiucuoshi_string += f"    - **{jijiu_i_type}**：{jijiu_i_method}\n"
        # 泄漏应急处理
        xielouyingjichuzhi = chemical["xielouyingjichuzhi"]
        # 灭火方法
        miehuofangfa = chemical["miehuofangfa"]
        st.markdown(
            f" **应急措施：**\n"
            f" - **急救**：\n{jijiucuoshi_string}"
            f" - **泄露**：{xielouyingjichuzhi}\n"
            f" - **灭火**：{miehuofangfa}"
        )
