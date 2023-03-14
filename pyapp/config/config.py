#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 16:54:23
LastEditTime: 2023-03-14 23:40:30
Description: 配置文件
usage:
    from pyapp.config.config import Config
    print(Config.rootDir)
'''

import os
import getpass
import platform
import sys


class Config:
    '''配置文件'''

    ##
    # 程序基础配置信息
    ##
    appName = 'vue-pywebview-pyinstaller'  # 应用名称
    appVersion = "3.1.0"  # 应用版本号
    appPackage = 'vip.pangao'    # 应用包名，用于在本地电脑生成 vip.pangao.vue-pywebview-pyinstaller 唯一文件夹

    ##
    # 系统配置信息
    ##
    appSystem = platform.system()    # 本机系统类型
    codeDir = sys.path[0].replace('base_library.zip', '')    # 代码根目录
    appDir = codeDir.replace(appName+'.app/Contents/MacOS/', '')    # 程序所在绝对目录
    staticDir = os.path.join(codeDir, 'static')    # 程序包中的static文件夹的绝对路径
    storageDir = ''    # 电脑上的存储目录

    ##
    # 其他配置信息
    ##
    devEnv = True    # 是否为开发环境，不需要手动更改，在程序运行的时候自动判断
    devPort = '3000'    # 开发环境中的前端页面端口
    cryptoKey = '0123456789123456'    # 对Python字节码加密
    ifCoverDB = False    # 是否覆盖电脑上存储的数据库，默认不覆盖。只有在数据库改动非常大，不得已的情况下才建议覆盖数据库

    ##
    # 函数
    ##
    def init(self):
        '''初始化'''
        # 获取电脑上的存储目录
        self.getStorageDir()

    def getStorageDir(self):
        '''获取电脑上的存储目录'''
        if Config.appSystem == 'Darwin':
            # Mac系统
            user = getpass.getuser()
            storageDir = os.path.join('/', 'Users', user, 'Library', 'Application Support')
        else:
            # win系统
            storageDir = os.getenv('APPDATA')
        storageDir = os.path.join(storageDir, Config.appPackage+'.'+Config.appName)
        if not os.path.isdir(storageDir):
            os.mkdir(storageDir)
        Config.storageDir = storageDir
