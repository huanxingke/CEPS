# coding=utf8
"""
二次处理 json 文件
"""
import base64
import json
import os


with open(os.path.join("./static", "chemicals.json"), "r") as fp:
    chemicals_data = json.load(fp)
with open(os.path.join("./static", "chemicals-struct.json"), "r") as fp:
    molecular_formulas_data = json.load(fp)

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
    
    
new_chemicals = []
for chemical_index, chemical in enumerate(chemicals_data):
    # 分子式
    molecular_formula = []
    # CAS号, 部分化学品对应多个 CAS 号
    cas_numbers = chemical["cas_number"]
    for cas_number in cas_numbers:
        if cas_number in molecular_formulas_data:
            molecular_formula.append(molecular_formulas_data.get(cas_number).get("molecular_formula") or "")
    # 加入分子式
    chemical["molecular_formula"] = molecular_formula
    # 名称排序
    chemical["name"] = sorted(chemical["name"], key=lambda x: len(x))
    # 索引
    chemical["index"] = chemical_index
    new_chemicals.append(chemical)

with open("./static/chemicals-optimize.json", "w", encoding="utf-8") as fp:
    json.dump(new_chemicals, fp)
    