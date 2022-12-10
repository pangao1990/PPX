#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PyWebView/vue-pywebview-pyinstaller/pyapp/mainCEF.py
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2022-03-23 15:45:04
Description: 生成客户端主程序【CEF模式】
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import os
import sys

import webview

from api.api import API
from config.config import Config
import signal

# 目的是按Ctrl+C时退出，但该代码不起作用，保留代码用作提供思路
def sigterm_handler(_signo, _stack_frame):
    sys.exit(0)

signal.signal(signal.SIGTERM, sigterm_handler)

# 前端页面目录
if sys.flags.dev_mode:
    DEBUG = True
else:
    DEBUG = False


def WebViewApp():

    api = API()    # 本地接口
    cfg = Config()    # 配置文件

    template = os.path.join("http://127.0.0.1:3000/", "index.html") # 设置本地Vue3开发端口

    webview.create_window(title=cfg.appName, url=template, js_api=api)    # 创建窗口
    webview.start(debug=DEBUG, http_server=True)    # 启动窗口


if __name__ == "__main__":

    WebViewApp()
