#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 16:54:23
LastEditTime: 2024-09-24 11:26:58
Description: 配置文件
usage:
    from pyapp.config.config import Config
    print(Config.rootDir)
'''

import getpass
import os
import platform
import sys


class Config:
    '''配置文件'''

    ##
    # 程序基础配置信息
    ##
    appName = 'PPX'  # 应用名称
    appNameEN = 'ppx'    # 应用名称-英文（用于生成缓存文件夹，必须是英文）
    appVersion = "V5.1.0"  # 应用版本号
    appDeveloper = "PanGao"  # 应用开发者
    appBlogs = "https://blog.pangao.vip"  # 个人博客
    appPackage = 'vip.pangao'    # 应用包名，用于在本地电脑生成 vip.pangao.ppx 唯一文件夹
    appUpdateUrl = 'https://api.github.com/repos/pangao1990/ppx/releases/latest'    # 获取程序更新信息 https://api.github.com/repos/pangao1990/ppx/releases/latest
    appISSID = 'F35003AB-441A-C0A6-4527-937E6A02F789'    # Inno Setup 打包唯一编号。在执行 pnpm run init 之前，请设置为空，程序会自动生成唯一编号，生成后请勿修改！！！

    ##
    # 系统配置信息（不需要修改，可以自动获取）
    ##
    cpuArch = platform.processor()    # 本机CPU架构
    appSystem = platform.system()    # 本机系统类型
    appIsMacOS = appSystem == 'Darwin'    # 是否为macOS系统
    codeDir = sys.path[0].replace('base_library.zip', '')    # 代码根目录，一般情况下，也是程序所在的绝对目录（但在build:pure打包成的独立exe程序中，codeDir是执行代码的缓存根目录，而非程序所在的绝对目录）
    staticDir = os.path.join(codeDir, 'static')    # 代码根目录下的static文件夹的绝对路径
    appDataDir = ''    # 电脑上可持久使用的隐藏目录
    downloadDir = ''    # 电脑上的下载目录

    ##
    # 其他配置信息
    ##
    devPort = '5173'    # 开发环境中的前端页面端口
    devEnv = True    # 是否为开发环境，不需要手动更改，在程序运行的时候自动判断
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
            downloadDir = os.path.join('/', 'Users', user, 'Downloads')
            appDataDir = os.path.join('/', 'Users', user, 'Library', 'Application Support', Config.appPackage+'.'+Config.appNameEN)
        elif Config.appSystem == 'Windows':
            # win系统
            downloadDir = os.path.join(os.getenv('USERPROFILE'), 'Downloads')
            appDataDir = os.path.join(os.getenv('APPDATA'), Config.appPackage+'.'+Config.appNameEN)
        elif Config.appSystem == 'Linux':
            # linux系统
            downloadDir = os.path.join(os.getenv('HOME'), 'Downloads')
            appDataDir = os.path.join(os.getenv('HOME'), '.'+Config.appPackage+'.'+Config.appNameEN)
        if not os.path.isdir(appDataDir):
            os.mkdir(appDataDir)
        Config.appDataDir = appDataDir    # 电脑上可持久使用的隐藏目录
        Config.downloadDir = downloadDir    # 电脑上的下载目录
