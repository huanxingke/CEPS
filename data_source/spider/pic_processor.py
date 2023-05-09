# coding=utf8
"""
裁剪结构式图片
"""
from PIL import Image
import numpy as np
import os


if not os.path.exists("struct_pic2"):
    os.mkdir("struct_pic2")

imagesDirectory = "struct_pic"

i = 0
for imageName in os.listdir(imagesDirectory):
    imagePath = os.path.join(imagesDirectory, imageName)
    origin = Image.open(imagePath)
    image = origin.convert("1")
    ImageArray = np.array(image)
    height = ImageArray.shape[0]
    width = ImageArray.shape[1]
    points = []
    for h in range(height):
        for w in range(width):
            point = image.getpixel((w, h))
            if point == 0:
                points.append([w, h])
    x = min([i[0] for i in points])
    x_w = max([i[0] for i in points])
    y = min([i[1] for i in points])
    y_h = max([i[1] for i in points])
    box = (
        x-2 if x >= 2 else x,
        y-2 if y >= 2 else y,
        x_w + 2 if x_w + 2 <= width else x_w,
        y_h + 2 if y_h + 2 <= height else y_h
    )
    cropped = origin.crop(box)
    cropped.save(r"struct_pic2\{}".format(imageName))
    print(f"{imageName} completed!")