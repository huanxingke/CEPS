## 使用方法

```[python]
from Webdav import JianGuoYunClient

# 注意:
#   本类主要应用于应急预案系统
#   所以所有文件默认位置为:
#   "我的坚果云/EmergencySystemData/"

# 根据账户密码实例化
jgy = JianGuoYunClient(
    username="{坚果云盘账户}", 
    password="{坚果云盘应用密码}"
)

# 任何时候都得先进行登录
login_res = jgy.login()
print(login_res)

# 上传一个纯文本文件
text = "我的坚果云"
# 必须传入 bytes 形式
upload_res = jgy.upload(content=text.encode(), filename="{文件名}")
print(upload_res)

# 删除一个文件
remove_res = jgy.remove("{文件名}")
print(remove_res)

# 获取一个纯文本文件内容
get_res = jgy.get(filename="{文件名}")
print(get_res)

# 格式化储存的所有文件
format_res = jgy.format()
print(format_res)
```

