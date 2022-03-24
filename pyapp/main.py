#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PyWebView/vue-pywebview-pyinstaller/pyapp/main.py
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2022-03-23 15:45:09
Description: 生成客户端主程序
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import os
import sys

import webview

from api.api import API
from config.config import Config

# 前端页面目录
if sys.flags.dev_mode:
    MAIN_DIR = os.path.join("..", "dist")  # 开发环境
    DEBUG = True
else:
    MAIN_DIR = os.path.join(".", "web")  # 生产环境
    DEBUG = False


def WebViewApp():

    api = API()    # 本地接口
    cfg = Config()    # 配置文件

    template = os.path.join(MAIN_DIR, "index.html")    # 设置页面，可以指向远程或本地

    webview.create_window(title=cfg.appName, url=template, js_api=api)    # 创建窗口
    webview.start(debug=DEBUG, http_server=True)    # 启动窗口


if __name__ == "__main__":

    WebViewApp()
