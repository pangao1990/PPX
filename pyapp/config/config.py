#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 16:54:23
LastEditTime: 2023-03-12 22:31:36
Description: 配置文件
usage:
    from pyapp.config.config import Config
    print(Config.rootDir)
'''

import os
import platform
import sys


class Config:
    '''配置文件'''

    ##
    # 程序基础配置信息
    ##
    appName = 'vue-pywebview-pyinstaller'  # 应用名称
    appVersion = "3.0.0"  # 应用版本号

    ##
    # 系统配置信息
    ##
    appSystem = platform.system()    # 本机系统类型
    codeDir = sys.path[0].replace('base_library.zip', '')    # 代码根目录
    appDir = codeDir.replace(appName+'.app/Contents/MacOS/', '')    # 程序所在绝对目录
    staticDir = os.path.join(codeDir, 'static')    # static文件夹的绝对路径

    ##
    # 其他配置信息
    ##
    devPort = '3000'    # 开发环境中的前端页面端口
    devEnv = True    # 是否为开发环境
    cryptoKey = '0123456789123456'    # 对Python字节码加密
