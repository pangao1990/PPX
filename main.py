#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 15:41:46
LastEditTime: 2022-12-29 16:55:13
Description: 生成客户端主程序
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 pywebview 模块。
'''

import argparse
import os
import sys

import webview
from api.api import API
from pyapp.config.config import Config


def WebViewApp(ifCef=False):

    api = API()    # 本地接口
    cfg = Config()    # 配置文件

    # 前端页面目录
    if sys.flags.dev_mode:
        MAIN_DIR = f'http://localhost:{cfg.devPort}/'  # 开发环境
        DEBUG = True
    else:
        MAIN_DIR = os.path.join(".", "web")  # 生产环境
        DEBUG = False

    template = os.path.join(MAIN_DIR, "index.html")    # 设置页面，可以指向远程或本地

    webview.create_window(title=cfg.appName, url=template, js_api=api)    # 创建窗口
    if ifCef:
        # CEF模式
        webview.start(debug=DEBUG, http_server=True, gui='cef')    # 启动窗口
    else:
        webview.start(debug=DEBUG, http_server=True)    # 启动窗口


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cef", action="store_true", dest="if_cef", help="if_cef")
    args = parser.parse_args()
    ifCef = args.if_cef

    WebViewApp(ifCef)
