#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 16:54:23
LastEditTime: 2022-12-29 16:36:54
Description: 配置文件
usage:
    from pyapp.config import Config
    cfg = Config()
'''

import platform


class Config:
    '''配置文件'''

    appName = 'vue-pywebview-pyinstaller'  # 应用名称
    appVersion = "2.0.0"  # 应用版本号

    devPort = '3000'    # 开发环境中的前端页面端口

    appSystem = platform.system()    # 本机系统类型
