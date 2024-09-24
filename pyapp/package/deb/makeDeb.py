#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2024-09-09 21:06:15
LastEditTime: 2024-09-09 23:37:41
Description: 制作linux下的deb安装包
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装  模块。
'''

import os
import sys

scriptDir = os.path.dirname(os.path.abspath(__file__))
pyappDir = os.path.dirname(os.path.dirname(scriptDir))
sys.path.append(pyappDir)
from config.config import Config

appName = Config.appName    # 应用名称
appVersion = Config.appVersion  # 应用版本号
appVersion = appVersion[1:]    # 去掉第一位V
appDeveloper = Config.appDeveloper  # 应用开发者
appBlogs = Config.appBlogs  # 个人博客

rootDir = os.path.dirname(pyappDir)
logoPath = os.path.join(rootDir, 'pyapp', 'icon', 'logo.png')


# 生成软件包的控制文件
getControl = f"""
Package: {appName}
Version: {appVersion}
Section: base
Priority: optional
Architecture: all
Depends: python3
Maintainer: {appDeveloper}
Description: {appBlogs}

"""
with open(os.path.join(scriptDir, 'control'), 'w+', encoding='utf-8') as f:
    f.write(getControl)


# 生成桌面文件
getDesktop = f"""
[Desktop Entry]
Name={appName}
Comment={appBlogs}
Exec=/opt/{appName}/bin/{appName}
Icon=/usr/share/icons/hicolor/128x128/apps/{appName}.png
Terminal=false
Type=Application
Categories=Utility;  # 选择适当的类别

"""
with open(os.path.join(scriptDir, f'{appName}.desktop'), 'w+', encoding='utf-8') as f:
    f.write(getDesktop)


# 生成安装完成调用的postinst脚本
getPostinst = """
# !/bin/bash
#更新桌面图标数据库
update-desktop-database /usr/share/applications || true
#获取当前的用户名
username=`getent passwd \`who\` | head -n 1 | cut -d : -f 1`
#判断桌面文件夹是否存在
if [ -d "/home/${username}/Desktop" ]; then
echo 'Desktop exist'
#将你的桌面文件复制到桌面
cp """ + f'/usr/share/applications/{appName}.desktop' + """ /home/${username}/Desktop
else
echo '桌面文件夹存在'
#中文系统自动复制到中文桌面
cp """ + f'/usr/share/applications/{appName}.desktop' + """ /home/${username}/桌面
fi

"""
with open(os.path.join(scriptDir, 'postinst'), 'w+', encoding='utf-8') as f:
    f.write(getPostinst)


buildDir = os.path.join(rootDir, 'build')

os.system(f'mkdir -p {buildDir}/bin && mv {buildDir}/{appName} {buildDir}/bin/{appName}')
os.system(f'mkdir -p {buildDir}/{appName}/DEBIAN')
os.system(f'mkdir -p {buildDir}/{appName}/opt/{appName}/bin')
os.system(f'mkdir -p {buildDir}/{appName}/usr/share/applications')
os.system(f'mkdir -p {buildDir}/{appName}/usr/share/icons/hicolor/128x128/apps')
os.system(f'cp {buildDir}/bin/{appName} {buildDir}/{appName}/opt/{appName}/bin/{appName}')
os.system(f'cp {scriptDir}/control {buildDir}/{appName}/DEBIAN/control')
os.system(f'cp {scriptDir}/postinst {buildDir}/{appName}/DEBIAN/postinst && chmod 755 {buildDir}/{appName}/DEBIAN/postinst')
os.system(f'cp {scriptDir}/{appName}.desktop {buildDir}/{appName}/usr/share/applications/{appName}.desktop')
os.system(f'cp {logoPath} {buildDir}/{appName}/usr/share/icons/hicolor/128x128/apps/{appName}.png')

os.system(f'cd {buildDir}')
os.system(f'cd {buildDir} && dpkg-deb --build {appName}')

os.system(f'rm -fr {buildDir}/{appName} && mv {buildDir}/bin/{appName} {buildDir}/{appName} && rm -fr {buildDir}/bin')

os.system(f'mv {buildDir}/{appName}.deb {buildDir}/{appName}-V{appVersion}_Linux.deb')
