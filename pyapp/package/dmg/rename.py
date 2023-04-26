#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PPX/pyapp/package/dmg/rename.py
Author: 潘高
LastEditors: 潘高
Date: 2023-04-24 21:15:12
LastEditTime: 2023-04-26 11:34:12
Description: 将 setup.dmg 改名为 PPX-V1.0.0_macOS.dmg
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装  模块。
        详细教程请移步至 https://blog.pangao.vip/Python环境搭建及模块安装/
'''

from pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent.parent))
from config.config import Config

cfg = Config()

appName = cfg.appName
appVersion = cfg.appVersion

buildDir = Path(Path(__file__).absolute().parent.parent.parent.parent.joinpath('build'))

ext = 'dmg'
appSys = 'macOS'

fromP = Path(buildDir.joinpath(f'setup.{ext}'))
toP = fromP.with_name(f'{appName}-{appVersion}_{appSys}.{ext}')

if fromP.exists():
    fromP.rename(toP)
