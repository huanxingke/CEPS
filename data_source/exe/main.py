# coding=utf8
from contextlib import closing
import subprocess
import zipfile
import base64
import shutil
import time
import sys
import re
import os

from PyQt5.QtGui import QTextCursor, QDesktopServices, QPixmap, QIcon
from PyQt5.QtCore import Qt, QUrl, QDateTime, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
import requests
import psutil

from app import Ui_mainframe
from get_pip import get_pip
import app_png


def ThreadErrorCatcher(func):
    """线程错误捕获"""
    def wrapper(self, *args, **kwargs):
        try:
            if kwargs:
                return func(self, *args, **kwargs)
            else:
                return func(self)
        except Exception as err:
            self.signal.emit({
                "code": -1,
                "msg": str(err)
            })
    return wrapper


def ErrorCatcher(func):
    """主程序错误捕获"""
    def wrapper(self, *args, **kwargs):
        try:
            if kwargs:
                return func(self, *args, **kwargs)
            else:
                return func(self)
        except Exception as err:
            self.showMessage(type=0, title="程序错误", msg=err)
    return wrapper


class Install(QThread):
    """安装线程"""
    signal = pyqtSignal(dict)

    def __init__(self, ctl, path):
        super(Install, self).__init__()
        self.ctl = ctl
        self.path = path

    def download(self, file_url, file_path, extract_path, attempts=1):
        # 下载, 显示进度条
        with closing(requests.get(url=file_url, stream=True)) as response:
            # github 有时候不返回数据, 需要重试
            if response.headers.get("content-length") is None:
                if attempts < 21:
                    self.signal.emit({
                        "code": 2,
                        "msg": f"数据下载失败，准备第{attempts}/20次重试..."
                    })
                    time.sleep(1)
                    return self.download(file_url=file_url, file_path=file_path, extract_path=extract_path, attempts=attempts+1)
                else:
                    raise Exception("已达最大重试次数，请稍后手动重试！")
            chunk_size = int(1024 * 1024 / 4)
            content_size = int(response.headers["content-length"]) / 1024 / 1024
            data_count = 0
            with open(file_path, "wb") as fp:
                counts = 0
                for data in response.iter_content(chunk_size=chunk_size):
                    fp.write(data)
                    data_count += len(data) / 1024 / 1024
                    now_jd = (data_count / content_size) * 100
                    self.signal.emit({
                        "code": 1,
                        "counts": counts,
                        "msg": "下载进度：{:.2f}%({:.2f}MB/{:.2f}MB)".format(now_jd, data_count, content_size)
                    })
                    counts += 1
        self.signal.emit({
            "code": 2,
            "msg": "下载完毕：{}".format(file_path)
        })
        # 解压
        self.signal.emit({
            "code": 2,
            "msg": "正在解压：{}".format(file_path)
        })
        f = zipfile.ZipFile(file_path)
        for file in f.namelist():
            f.extract(file, extract_path)
        f.close()
        # 解压完成后删除压缩包
        if os.path.exists(file_path):
            os.remove(file_path)
        self.signal.emit({
            "code": 2,
            "msg": "解压完成：{}".format(file_path)
        })

    def execute(self, cmd):
        """执行 cmd

        :param cmd: cmd 命令
        :return:
        """
        # 重定向输出管道
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for i in iter(pipe.stdout.readline, ""):
            # 解码
            i = i.decode("gbk").strip()
            # 不为空时输出完毕
            if pipe.poll() is not None:
                self.signal.emit({
                    "code": 2,
                    "msg": "执行完毕！"
                })
                break
            # 有内容时才输出
            if len(i) > 1:
                self.signal.emit({
                    "code": 3,
                    "msg": i
                })

    def getPip(self):
        """安装 pip"""
        # 修改三方库访问配置
        self.signal.emit({
            "code": 3,
            "msg": "正在设置三方库权限..."
        })
        with open(os.path.join(self.path, "env", "python310._pth"), "r") as fp:
            _pth = fp.read()
        _pth = _pth.replace("#import site", "import site")
        with open(os.path.join(self.path, "env", "python310._pth"), "w") as fp:
            fp.write(_pth)
        # 下载 pip
        self.signal.emit({
            "code": 3,
            "msg": "正在下载pip..."
        })
        with open(os.path.join(self.path, "env", "get-pip.py"), "w", encoding="utf-8") as fp:
            fp.write(get_pip)
        # 安装 pip
        self.signal.emit({
            "code": 3,
            "msg": "正在安装pip..."
        })
        cmd = f".\\{self.path}\\env\\python.exe .\\{self.path}\\env\\get-pip.py"
        self.execute(cmd)

    def installPackages(self):
        """安装依赖"""
        cmd = f".\\{self.path}\\env\\python.exe -m pip install -r .\\{self.path}\\CEPS-master\\requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple"
        self.execute(cmd)

    @ThreadErrorCatcher
    def run(self):
        self.signal.emit({
            "code": 0,
            "msg": "正在初始化项目路径..."
        })
        # 安装依赖
        if self.ctl == "python":
            # 下载并解压 python
            self.signal.emit({
                "code": 0,
                "msg": "正在初始化嵌入式Python环境..."
            })
            self.download(
                file_url="https://cdn.npmmirror.com/binaries/python/3.10.10/python-3.10.10-embed-amd64.zip",
                file_path=os.path.join(self.path, "env.zip"),
                extract_path=os.path.join(self.path, "env")
            )
            # 安装 pip
            self.signal.emit({
                "code": 0,
                "msg": "正在配置pip..."
            })
            self.getPip()
            self.signal.emit({
                "code": 200,
                "msg": "安装完毕！"
            })
        # 下载脚本
        else:
            self.signal.emit({
                "code": 0,
                "msg": "正在下载项目文件..."
            })
            self.download(
                file_url="https://codeload.github.com/huanxingke/CEPS/zip/refs/heads/master",
                file_path=os.path.join(self.path, "CEPS.zip"),
                extract_path=self.path
            )
            self.signal.emit({
                "code": 0,
                "msg": "下载完毕！"
            })
            # 安装依赖库
            self.signal.emit({
                "code": 0,
                "msg": "正在安装三方库..."
            })
            self.installPackages()
            self.signal.emit({
                "code": 200,
                "msg": "安装完毕！"
            })


class ExecuteCMD(QThread):
    """执行命令并返回控制台输出"""
    signal = pyqtSignal(dict)

    def __init__(self, cmd):
        super(ExecuteCMD, self).__init__()
        self.cmd = cmd

    @ThreadErrorCatcher
    def run(self):
        # 重定向输出管道
        pipe = psutil.Popen(self.cmd, shell=True, stdout=subprocess.PIPE)
        for i in iter(pipe.stdout.readline, ""):
            # 解码
            i = i.decode("gbk").strip()
            # 不为空时输出完毕
            if pipe.poll() is not None:
                self.signal.emit({
                    "code": 200,
                    "msg": i
                })
                break
            # 有内容时才输出
            if len(i) > 1:
                # 获取线程的子线程
                pipe_children = pipe.children()
                self.signal.emit({
                    "code": 0,
                    "msg": i,
                    "pipe": pipe,
                    "pipe_children": pipe_children
                })


class Processor(QWidget, Ui_mainframe):
    """主进程"""
    def __init__(self, mainframe):
        super(Processor, self).__init__()
        # 加载Ui
        self.setupUi(mainframe)
        self.mainframe = mainframe
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 初始化变量
        # 执行进程
        self.executeThreading = None
        # 安装进程
        self.installThreading = None
        # subprocess 管道
        self.pipe = None
        self.pipe_children = None
        # 包体完整性
        self.ceps = False
        self.python = False
        self.ctl = None
        # 软件数据路径
        # 项目路径
        self.ceps_path = "CEPS"
        # python 路径
        self.python_path = os.path.join(self.ceps_path, "env")
        # 绑定事件
        self.bindEvents()
        # 检索程序包是否完整
        self.checkPackage()

    def showMessage(self, type, title, msg):
        """消息弹窗

        :param type: 弹窗类型, 0 为警告, 其他为提示
        :param title: 弹窗标题
        :param msg: 弹窗消息
        :return:
        """
        if type == 0:
            QMessageBox.warning(
                self,
                title,
                str(msg),
                QMessageBox.Yes | QMessageBox.No
            )
        else:
            QMessageBox.information(
                self,
                title,
                str(msg),
                QMessageBox.Yes | QMessageBox.No
            )

    @ErrorCatcher
    def bindEvents(self):
        """事件绑定"""
        # 启动按钮
        self.startButton.clicked.connect(self.execute)
        # 安装依赖按钮
        self.installEnvButton.clicked.connect(lambda: self.install(ctl="python"))
        # 下载脚本按钮
        self.installScriptButton.clicked.connect(lambda: self.install(ctl="ceps"))
        # 监听退出事件
        self.mainframe.closeEvent = self.closeEvent

    @ErrorCatcher
    def checkPackage(self):
        """检索程序包是否完整"""
        self.printLogs(log="正在检查完整性...", color="blue")
        # 初始化文件夹
        if not os.path.exists(self.ceps_path):
            os.mkdir(self.ceps_path)
        if not os.path.exists(self.python_path):
            os.mkdir(self.python_path)
        # 检查 python 环境
        if os.path.exists(os.path.join(self.python_path, "python.exe")):
            self.python = True
            self.installEnvButton.setText("重装依赖")
        else:
            self.python = False
            self.printLogs(log="软件依赖缺失，请重新安装依赖！", color="red")
            self.startButton.setDisabled(True)
            self.installEnvButton.setText("安装依赖")
        # 检查项目脚本
        if os.path.exists(os.path.join(self.ceps_path, "CEPS-master", "CEPS.py")):
            self.ceps = True
            self.installScriptButton.setText("更新脚本")
        else:
            self.ceps = False
            self.printLogs(log="软件脚本缺失，请重新下载脚本！", color="red")
            self.startButton.setDisabled(True)
            self.installScriptButton.setText("下载脚本")
        if self.python and self.ceps:
            self.printLogs(log="项目可执行！", color="green")
            self.startButton.setDisabled(False)
            try:
                with open(os.path.join(self.ceps_path, "CEPS-master", "version"), "r") as fp:
                    version = fp.read()
                    self.printLogs(log=f"版本：{version}", color="green")
            except:
                pass

    def printLogs(self, log, color=None, flush=False):
        """实时打印日志

        :param log: 日志内容
        :param color: 颜色
        :param flush: 是否刷新最后一行
        :return:
        """
        # 显示日期
        current_time = QDateTime.currentDateTime()
        timeDisplay = current_time.toString("hh:mm:ss")
        log = "[{}] {}".format(timeDisplay, log)
        # 只保留 200 条日志
        if self.logsBrowser.document().lineCount() >= 200:
            self.logsBrowser.document().clear()
            self.logsBrowser.append("<p style='color:red'>------日志过多, 已保留最近 200 条日志!------</p>")
        # 是否刷新输出最后一行
        if flush:
            html = self.logsBrowser.toHtml()
            plist = re.compile(r"<p(.*?)/p>").findall(html)
            plist = plist[:(len(plist) - 1)]
            self.logsBrowser.clear()
            for p in plist:
                self.logsBrowser.append(f"<p{p}/p>")
        # 是否设置颜色
        if not color:
            self.logsBrowser.append("<p style='color:black'>{}</p>".format(log))
        else:
            self.logsBrowser.append("<p style='color:{}'>{}</p>".format(color, log))
        # 移动指针到最后一行
        cursor = QTextCursor(
            self.logsBrowser.document().findBlockByLineNumber(self.logsBrowser.document().lineCount() - 1)
        )
        self.logsBrowser.setTextCursor(cursor)

    def installCallback(self, result):
        """安装线程的反馈函数"""
        msg = result["msg"]
        code = result["code"]
        if code == 200:
            if self.ctl == "python":
                self.installEnvButton.setText("重装依赖")
            else:
                self.installScriptButton.setText("更新脚本")
            self.printLogs(log=msg, color="blue")
            if self.installThreading and self.installThreading.isRunning():
                self.installThreading.quit()
                self.installThreading.terminate()
            self.checkPackage()
        elif code == 0:
            self.printLogs(log=msg, color="blue")
        elif code == 1:
            flush = True if result["counts"] > 0 else False
            self.printLogs(log=msg, flush=flush)
        elif code == 2:
            self.printLogs(log=msg, color="orange")
        elif code == 3:
            self.printLogs(log=msg)
        else:
            if self.ctl == "python":
                self.installEnvButton.setText("安装依赖")
            else:
                self.installScriptButton.setText("下载脚本")
            self.showMessage(type=0, title="程序错误", msg=msg)
            self.printLogs(log=msg, color="red")
            self.printLogs(log="重试或许可以解决此问题...", color="blue")
            if self.installThreading and self.installThreading.isRunning():
                self.installThreading.quit()
                self.installThreading.terminate()
            self.checkPackage()

    @ErrorCatcher
    def install(self, ctl):
        """启动安装线程"""
        for threading in [self.executeThreading, self.installThreading]:
            if (threading is not None) and threading.isRunning():
                self.showMessage(type=0, title="温馨提示", msg="请等待线程执行完毕！")
                return
        self.printLogs(log="准备安装...", color="blue")
        self.ctl = ctl
        if ctl == "python":
            self.installEnvButton.setText("正在安装")
        else:
            self.installScriptButton.setText("正在下载")
        self.installThreading = Install(ctl=ctl, path=self.ceps_path)
        self.installThreading.start()
        self.installThreading.signal.connect(self.installCallback)

    def killPipe(self):
        """终止命令行线程"""
        if self.pipe_children is not None:
            # 终止子线程
            for pipe_children in self.pipe_children:
                try:
                    pipe_children.terminate()
                    pipe_children.wait()
                    pipe_children.kill()
                except:
                    pass
            # 终止线程
            if self.pipe is not None:
                try:
                    self.pipe.terminate()
                    self.pipe.wait()
                    self.pipe.kill()
                except:
                    pass

    @ErrorCatcher
    def shutdown(self):
        """启动终止执行线程"""
        # 终止命令行线程
        self.killPipe()
        # 终止 qt 线程
        if self.executeThreading and self.executeThreading.isRunning():
            self.executeThreading.quit()
            self.executeThreading.terminate()
            self.printLogs(log="已终止线程！", color="green")
        # 绑定为启动程序
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(self.execute)
        self.startButton.setText("启动程序")
        # 恢复默认链接文字
        self.localUrl.setText("待识别")
        self.networkUrl.setText("待识别")
        try:
            self.localUrl.clicked.disconnect()
            self.networkUrl.clicked.disconnect()
        except:
            pass

    # 反馈函数
    def executeCallback(self, result):
        local_url_pattern = re.compile(r"Local URL: (.*)")
        network_url_pattern = re.compile(r"Network URL: (.*)")
        msg = result["msg"]
        code = result["code"]
        if code == -1:
            self.showMessage(type=0, title="程序错误", msg=msg)
            self.printLogs(log=msg, color="red")
        elif code == 0:
            self.printLogs(log=msg)
            # 线程
            self.pipe = result["pipe"]
            # 线程的子线程
            self.pipe_children = result["pipe_children"]
            # 提取链接
            local_url = local_url_pattern.findall(msg)
            network_url = network_url_pattern.findall(msg)
            if local_url:
                self.localUrl.setText(local_url[0])
                self.localUrl.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(local_url[0])))
            elif network_url:
                self.networkUrl.setText(network_url[0])
                self.networkUrl.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(network_url[0])))
        else:
            self.printLogs(log="执行完毕！", color="green")
            self.shutdown()

    @ErrorCatcher
    def execute(self):
        """启动执行命令线程"""
        if self.installThreading and self.installThreading.isRunning():
            self.showMessage(type=0, title="温馨提示", msg="请等待其他线程执行完毕！")
            return
        if not os.path.exists("app.bat"):
            with open("app.bat", "w", encoding="utf-8") as fp:
                fp.write(
                    r"cd .\\CEPS\\CEPS-master && ..\\env\\Scripts\\streamlit run CEPS.py"
                )
        with open("app.bat", "r", encoding="utf-8") as fp:
            cmd = fp.read()
        self.printLogs(log="准备执行...", color="blue")
        # 绑定为终止程序
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(self.shutdown)
        self.startButton.setText("终止程序")
        # 启动线程
        self.executeThreading = ExecuteCMD(cmd=cmd)
        self.executeThreading.start()
        self.executeThreading.signal.connect(self.executeCallback)

    def closeEvent(self, event):
        """程序退出事件"""
        reply = QMessageBox.question(
            self,
            "提示",
            "是否退出程序？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # 退出前终止 streamlit 线程
            self.killPipe()
            event.accept()
            sys.exit(0)
        else:
            event.ignore()


# py文件中的base64数据转图片对象
def py2pic(img):
    imgData = base64.b64decode(img)
    img = QPixmap()
    img.loadFromData(imgData)
    return img


if __name__ == "__main__":
    # 创建 PyQt 进程
    app = QApplication(sys.argv)
    # 设置图标
    app.setWindowIcon(QIcon(py2pic(app_png.img)))
    # 防止卡死
    app.processEvents()
    # 初始化组件
    form = QWidget()
    w = Processor(form)
    # 展示窗口
    form.show()
    # 监听退出事件
    sys.exit(app.exec_())