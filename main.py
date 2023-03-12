#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2023-03-12 21:42:05
Description: 生成客户端主程序
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import argparse
import os
import sys

import webview

from api.api import API
from pyapp.config.config import Config
from pyapp.db.db import DB

db = DB()    # 数据库类


def on_shown():
    # print('程序启动')
    db.connect()    # 连接数据库


def on_loaded():
    # print('DOM加载完毕')
    pass


def on_closing():
    # print('程序关闭')
    db.close()    # 关闭数据库


def WebViewApp(ifCef=False):

    api = API()    # 本地接口

    # 是否为开发环境
    Config.devEnv = sys.flags.dev_mode

    # 前端页面目录
    if Config.devEnv:
        # 开发环境
        MAIN_DIR = f'http://localhost:{Config.devPort}/'
        template = os.path.join(MAIN_DIR, "")    # 设置页面，指向远程
    else:
        # 生产环境
        MAIN_DIR = os.path.join(".", "web")
        template = os.path.join(MAIN_DIR, "index.html")    # 设置页面，指向本地

    # 创建窗口
    window = webview.create_window(title=Config.appName, url=template, js_api=api, width=1000, height=700, min_size=(800,600))

    # 获取窗口实例
    API.window = window

    # 绑定事件
    window.events.shown += on_shown
    window.events.loaded += on_loaded
    window.events.closing += on_closing

    # CEF模式
    guiCEF = 'cef' if ifCef else None

    # 启动窗口
    webview.start(debug=Config.devEnv, http_server=True, gui=guiCEF)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cef", action="store_true", dest="if_cef", help="if_cef")
    args = parser.parse_args()

    ifCef = args.if_cef    # 是否开启cef模式

    WebViewApp(ifCef)
