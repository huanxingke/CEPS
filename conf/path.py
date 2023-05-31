# coding=utf8
"""
配置: 文件(夹)路径
"""
from pathlib import Path
import os


# 根
root_path = Path(os.path.dirname(os.path.abspath(__file__))).parent

# 静态文件
static_path = os.path.join(root_path, "static")

# 字体文件
fonts_path = os.path.join(static_path, "fonts")

# 图片
images_path = os.path.join(static_path, "images")
# 公共
images_common_path = os.path.join(images_path, "common")
# 结构式
images_struct_path = os.path.join(images_path, "struct_pic")
# ghs
images_ghs_path = os.path.join(images_path, "GHSPic")
# 知识库
images_learning_path = os.path.join(images_path, "learning")
# md 文件内的图片
images_knowledge_path = os.path.join(images_path, "knowledge")

# JSON 文件
json_path = os.path.join(static_path, "json")
# 考试系统需要用到的 JSON 文件
json_exam_path = os.path.join(json_path, "exam")

# md 文件
md_path = os.path.join(static_path, "markdown")

# pdf 文件
pdf_path = os.path.join(static_path, "pdf")

# 模型文件
models_path = os.path.join(static_path, "models")
# 化学品检索模型
models_chemicals_path = os.path.join(models_path, "chemicals")
# 案例检索模型
models_cases_path = os.path.join(models_path, "cases")