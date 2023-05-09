# coding=utf8
"""
虚拟请求
"""
import urllib3
# 取消警告提示
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import datetime
import time
import json
import os
import re

from retrying import retry
import requests


class FakeIP(object):
    """获取代理 ip"""
    def __init__(self):
        # 初始化账号配置
        self.params = {
            "order_id": "53692",
            "username": "乘风之梦",
            "md5": "a06d842639872ca246c777638871fe09",
            "timestamp": int(time.time())
        }

    def getProxies(self):
        """重新获取 ip"""
        try:
            url = "https://apis.engeniusiot.com/api/getips"
            request = requests.get(url=url, params=self.params)
            proxy_dict = request.json()
            if proxy_dict["code"] == 0:
                host = proxy_dict["data"]["proxy_list"][0]["host"]
                port = proxy_dict["data"]["proxy_list"][0]["port"]
                proxy = host + ":" + str(port)
                proxies = {
                    "http": proxy,
                    "https": proxy
                }
                with open("./static/fakeip.json", "w", encoding="utf-8") as fp:
                    json.dump(proxies, fp)
                print(proxies)
                print(self.check_order())
                return proxies
            else:
                with open("./static/fakeip.json", "w", encoding="utf-8") as fp:
                    json.dump({}, fp)
                return {}
        except:
            return {}

    def getLocalProxies(self):
        """获取本地缓存的 ip"""
        if os.path.exists("./static/fakeip.json"):
            with open("./static/fakeip.json", "r", encoding="utf-8") as fp:
                try:
                    proxies = json.load(fp)
                except:
                    proxies = self.getProxies()
        else:
            proxies = self.getProxies()
        return proxies

    def check_order(self):
        """查询 ip 订单"""
        url = "https://apis.engeniusiot.com/api/getorderinfo"
        request = requests.get(url=url, params=self.params)
        order_dict = request.json()
        left_count = order_dict["data"]["left_count"]
        expire_time = int(order_dict["data"]["expire_time"] / 1000)
        left_time = self.transTimeStamp(expire_time)
        return {"left_count": left_count, "left_time": left_time}

    @staticmethod
    def transTimeStamp(timeStamp):
        """转换日期"""
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        formatTime = dateArray.strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]
        timeNow = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).split(" ")[0]
        deadline = time.strptime(formatTime, "%Y-%m-%d")
        dateNow = time.strptime(timeNow, "%Y-%m-%d")
        deadline = datetime.datetime(deadline[0], deadline[1], deadline[2])
        dateNow = datetime.datetime(dateNow[0], dateNow[1], dateNow[2])
        left = str(deadline - dateNow).split(" ")[0]
        return left


def retryCallback(attempts, delay):
    """重试回调函数

    :param attempts: 重试次数, 回调时自动传入
    :param delay: 重试耗时, 回调时自动传入
    :return:
    """
    if attempts > 15:
        raise Exception("请求已达最大重试次数!")
    time.sleep(2)
    # 重新获取 ip
    FakeIP().getProxies()


# stop_func: 重试回调函数
@retry(wait_random_min=2000, wait_random_max=5000, stop_func=retryCallback)
def fakeRequests(url, headers=None, data=None, params=None,
                 json_data=None, methods="GET", allow_redirects=True,
                 cookies=None, need_proxies=False, timeout=3):
    """封装发送请求的函数

    :param str url: 请求链接
    :param dict headers: 请求头
    :param dict data: form data 类型数据
    :param dict params: url 参数型数据
    :param dict json_data: json 类型数据
    :param str methods: 请求方法, "POST" 或 "GET"
    :param bool allow_redirects: 是否允许重定向
    :param cookies: cookiejar
    :param need_proxies: 是否使用代理 ip
    :param timeout: 超时时间
    :return: requests.response 对象
    """
    proxies = {}
    if need_proxies:
        proxies = FakeIP().getLocalProxies()
    if methods in ["POST", "post"]:
        response = requests.post(url=url, headers=headers, data=data,
                                 params=params, json=json_data, proxies=proxies,
                                 cookies=cookies, allow_redirects=allow_redirects, timeout=timeout)
    else:
        response = requests.get(url=url, headers=headers, params=params,
                                proxies=proxies, allow_redirects=allow_redirects,
                                cookies=cookies, timeout=timeout)
    if re.compile("hxp\.nrcc\.com\.cn").findall(url):
        if response.json()["errMsg"] != "success":
            raise Exception(response.json()["errMsg"])
    else:
        if response.status_code not in [200, 404]:
            raise Exception(str(response.status_code))
    return response
