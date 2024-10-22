#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 09:05:53
LastEditTime: 2024-10-22 21:05:38
Description: 生成 .json dmg配置文件
        详细规范：
            title               （字符串，必填）-已生产的DMG的标题，安装时将显示
            icon                （字符串，可选）-图标的路径，挂载时将显示
            background          （字符串，可选）-您的背景路径
            background-color    （字符串，可选）-背景颜色（接受css颜色）
            icon-size           （数字，可选）-DMG内所有图标的大小
            window              （对象，可选）-窗口选项
                position        （对象，可选）-打开时的位置
                    x           （数字，必填）-相对于屏幕左侧的X位置
                    y           （数字，必填）-相对于屏幕底部的Y位置
                size            （对象，可选）-窗口大小
                    width       （数字，必填）-窗口宽度
                    height      （数字，必填）-窗口高度
            format              （枚举[字符串]，可选）-磁盘映像格式
                UDRW             UDIF读/写图像
                UDRO             UDIF只读图像
                UDCO             UDIF ADC压缩图像
                UDZO             UDIF zlib压缩图像
                UDBZ             UDIF bzip2压缩图像（仅限OS X 10.4+）
                ULFO             UDIF lzfse压缩图像（仅限OS X 10.11+）
                ULMO             UDIF lzma压缩图像（仅限macOS 10.15+）
            filesystem          （枚举[字符串]，可选）-磁盘映像文件系统
                HFS+
                APFS            （仅限macOS 10.13+）
            contents            （数组[对象]，必填）-这是您的DMG的内容。
                x               （数字，必填）-相对于图标中心的X位置
                y               （数字，必填）-相对于图标中心的Y位置
                type            （enum[字符串]，必填）
                    link         创建指向指定目标的链接
                    file         将文件添加到DMG
                    position     放置当前文件
                path            （字符串，必填）-文件的路径
                name            （字符串，可选）-DMG中的文件名称
            code-sign           （对象，可选）-共同设计DMG的选项
                signing-identity（字符串，必填）-签署结果DMG的身份
                identifier      （字符串，可选）-显式设置嵌入代码签名中的唯一标识符字符串
'''

import os
import sys

pyappDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(pyappDir)

from config.config import Config

appName = Config.appName    # 应用名称
appVersion = Config.appVersion    # 应用版本号

dmgName = f'{appName}-{appVersion}_macOS'


# 获取配置文件内容
def getJson():
    return """
filename = '""" + dmgName + """'
volume_name = '""" + dmgName + """.dmg'
format = 'UDBZ'
files = ['""" + pyappDir + """/../build/""" + appName + """.app', '""" + pyappDir + """/package/dmg/潘高的小站.webloc']
symlinks = {'Applications': '/Applications'}
icon_locations = {
    '""" + appName + """.app': (160, 120),
    'Applications': (430, 120),
    '潘高的小站.webloc': (450, 243)
}
window_rect = ((200, 200), (590, 416))
icon_size = 60
text_size = 12
badge_icon = '""" + pyappDir + """/icon/logo.icns'
background = '""" + pyappDir + """/package/dmg/bg.png'
"""


# 生成配置文件
jsonDir = os.path.dirname(__file__)
with open(os.path.join(jsonDir, 'dmg.py'), 'w+', encoding='utf-8') as f:
    f.write(getJson())
