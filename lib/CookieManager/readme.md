## 获取 cookie

```[python]
from CookieManager import CookieManager

cm = CookieManager()
cookie_res = cm.get("{cookie键}")
if cookie_res and cookie_res.get("code") == 200:
    # 设置 cookie 时对值 b64encode 了
    # 所以得先解密
    cookie_value = base64.b64decode(cookie_res["value"]).decode()
```

## 设置 cookie

```[python]
from CookieManager import JSCookieManager

# 注意 cookie 值必须为字符串的形式
# JSCookieManager 方法内部会将 cookie 值进行 b64encode
JSCookieManager(
    key="{cookie键}", 
    value="{cookie值}"
)
```

