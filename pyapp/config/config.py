#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 16:54:23
LastEditTime: 2023-04-26 18:28:48
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
    appName = 'PPX'  # 应用名称
    appNameEN = 'ppx'    # 应用名称-英文（用于生成缓存文件夹，必须是英文）
    appVersion = "V1.0.0"  # 应用版本号
    appDeveloper = "PanGao"  # 应用开发者
    appBlogs = "https://blog.pangao.vip"  # 个人博客
    appPackage = 'vip.pangao'    # 应用包名，用于在本地电脑生成 vip.pangao.ppx 唯一文件夹
    appUpdateUrl = 'https://api.github.com/repos/pangao1990/ppx/releases/latest'    # 获取程序更新信息 https://api.github.com/repos/pangao1990/ppx/releases/latest
    appISSID = ''    # Inno Setup 打包唯一编号，可由 apyapp/package/exe/getAppISSID.py 生成，生成后，请勿修改！！！

    ##
    # 系统配置信息
    ##
    appSystem = platform.system()    # 本机系统类型
    appIsMacOS = appSystem == 'Darwin'    # 是否为macOS系统
    codeDir = sys.path[0].replace('base_library.zip', '')    # 代码根目录
    appDir = codeDir.replace(appName+'.app/Contents/MacOS/', '')    # 程序所在绝对目录
    staticDir = os.path.join(codeDir, 'static')    # 程序包中的static文件夹的绝对路径
    storageDir = ''    # 电脑上的存储目录
    downloadDir = ''    # 电脑上的下载目录

    ##
    # 其他配置信息
    ##
    devEnv = True    # 是否为开发环境，不需要手动更改，在程序运行的时候自动判断
    devPort = '5173'    # 开发环境中的前端页面端口
    cryptoKey = '0123456789123456'    # 对Python字节码加密 0123456789123456
    ifCoverDB = False    # 是否覆盖电脑上存储的数据库，默认不覆盖。只有在数据库改动非常大，不得已的情况下才建议覆盖数据库

    ##
    # 函数
    ##
    def init(self):
        '''初始化'''
        # 获取电脑上的目录
        self.getDir()

    def getDir(self):
        '''获取电脑上的目录'''
        if Config.appSystem == 'Darwin':
            # Mac系统
            user = getpass.getuser()
            storageDir = os.path.join('/', 'Users', user, 'Library', 'Application Support')
            downloadDir = os.path.join('/', 'Users', user, 'Downloads')
        else:
            # win系统
            storageDir = os.getenv('APPDATA')
            downloadDir = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
        storageDir = os.path.join(storageDir, Config.appPackage+'.'+Config.appNameEN)
        if not os.path.isdir(storageDir):
            os.mkdir(storageDir)
        Config.storageDir = storageDir    # 电脑上的存储目录
        Config.downloadDir = downloadDir    # 电脑上的下载目录
