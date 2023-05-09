# coding=utf8
"""
生成临界量 json
"""
import json


def initCriticalQuantity():
    with open("./static/chemicals-optimize.json", "r", encoding="utf-8") as fp:
        chemicals = json.load(fp)
    chemicals_with_critical_quantity = []
    for chemical in chemicals:
        name = chemical["name"][0]
        critical_quantity = chemical["critical_quantity"]
        if critical_quantity:
            chemicals_with_critical_quantity.append({
                "name": name,
                "critical_quantity": round(float(critical_quantity), 2)
            })
    with open("./static/critical-quantity.json", "w", encoding="utf-8") as fp:
        json.dump(chemicals_with_critical_quantity, fp)


if __name__ == '__main__':
    initCriticalQuantity()