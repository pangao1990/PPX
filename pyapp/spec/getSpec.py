#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-23 09:05:53
LastEditTime: 2024-09-08 20:47:03
Description: 生成 .spec APP配置文件
'''

import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mac", action="store_true", dest="if_mac", help="if_mac")
parser.add_argument("-l", "--linux", action="store_true", dest="if_linux", help="if_linux")
args = parser.parse_args()
ifMac = args.if_mac
ifLinux = args.if_linux

buildPath = 'build'    # 存放最终打包成app的相对路径
console = False    # 是否展示终端
appName = Config.appName    # 项目名称
version = Config.appVersion    # 版本号
logoExt = 'icns' if ifMac else 'png' if ifLinux else 'ico'

# 添加文件到打包中
addDll = ''
# 添加文件夹到打包中
addModules = "('../../gui/dist', 'web'), ('../../static', 'static')"


# spec配置文件 前半部分通用格式
def specFirstPart():
    return f'''
# -*- mode: python ; coding: utf-8 -*-

import os

import PyInstaller.config

# 存放最终打包成app的相对路径
buildPath = '{buildPath}'
PyInstaller.config.CONF['distpath'] = buildPath

# 存放打包成app的中间文件的相对路径
cachePath = os.path.join(buildPath, 'cache')
if not os.path.exists(cachePath):
    os.makedirs(cachePath)
PyInstaller.config.CONF['workpath'] = cachePath

# icon相对路径
icoPath = os.path.join('..', 'icon', 'logo.{logoExt}')

# 项目名称
appName = '{appName}'

# 版本号
version = '{version}'


a = Analysis(['../../main.py'],
            pathex=[],
            binaries=[{addDll}],
            datas=[{addModules}],
            hiddenimports=[],
            hookspath=[],
            hooksconfig={{}},
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            noarchive=False)
pyz = PYZ(a.pure, a.zipped_data)

'''


# 打包为一个APP文件
def specPackagePartAPP():
    return f'''
exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=appName,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console={console},
        disable_windowed_traceback=False,
        target_arch=None,  # x86_64, arm64, universal2
        codesign_identity=None,
        entitlements_file=None)
coll = COLLECT(exe,
                a.binaries,
                a.zipfiles,
                a.datas,
                strip=False,
                upx=True,
                upx_exclude=[],
                name=appName)
app = BUNDLE(coll,
            name=appName+'.app',
            icon=icoPath,
            version=version,
            bundle_identifier=None)

'''


# 打包为一个exe文件
def specPackagePartEXE():
    return f'''
exe = EXE(pyz,
        a.scripts,
        a.binaries,
        a.zipfiles,
        a.datas,
        [],
        name=appName,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        upx_exclude=[],
        runtime_tmpdir=None,
        console={console},
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icoPath)

'''


# 以文件夹形式存在
def specUnpackagePartEXE():
    return f'''
exe = EXE(pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name=appName,
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console={console},
        disable_windowed_traceback=False,
        target_arch=None,
        codesign_identity=None,
        entitlements_file=None,
        icon=icoPath)
coll = COLLECT(exe,
            a.binaries,
            a.zipfiles,
            a.datas,
            strip=False,
            upx=True,
            upx_exclude=[],
            name=appName)

'''


# 生成 spec 配置文件
specDir = os.path.dirname(__file__)


if ifMac:
    console = False    # 是否展示终端
    # macos.spec
    with open(os.path.join(specDir, 'macos.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartAPP())

    console = True    # 是否展示终端
    # macos-pre.spec 带终端
    with open(os.path.join(specDir, 'macos-pre.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartAPP())
elif ifLinux:
    console = False    # 是否展示终端
    # linux.spec
    with open(os.path.join(specDir, 'linux.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())

    console = True    # 是否展示终端
    # linux-pre.spec 带终端
    with open(os.path.join(specDir, 'linux-pre.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())
else:
    console = False    # 是否展示终端
    # windows.spec
    with open(os.path.join(specDir, 'windows.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())
    # windows-folder.spec
    with open(os.path.join(specDir, 'windows-folder.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specUnpackagePartEXE())

    console = True    # 是否展示终端
    # windows-pre.spec 带终端
    with open(os.path.join(specDir, 'windows-pre.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())
    # windows-folder-pre.spec
    with open(os.path.join(specDir, 'windows-folder-pre.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specUnpackagePartEXE())

    console = False    # 是否展示终端
    # 添加缺失的动态链接库
    addDll = """
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/icudtl.dat', './'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/natives_blob.bin','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/subprocess.exe','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/libcef.dll','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/chrome_elf.dll','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/v8_context_snapshot.bin','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/cef.pak','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/cef_100_percent.pak','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/cef_200_percent.pak','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/cef_extensions.pak','./'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/icudtl.dat', './cefpython3'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/natives_blob.bin','./cefpython3'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/locales/en-US.pak','./locales'),
        ('../../pyapp/pyenv/pyenvCEF/Lib/site-packages/cefpython3/locales/zh-CN.pak','./locales')
    """
    # windows-pre.spec 带终端
    with open(os.path.join(specDir, 'windows-cef.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())
    # windows-folder-pre.spec
    with open(os.path.join(specDir, 'windows-folder-cef.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specUnpackagePartEXE())

    console = True    # 是否展示终端
    # windows-pre.spec 带终端
    with open(os.path.join(specDir, 'windows-pre-cef.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specPackagePartEXE())
    # windows-folder-pre.spec
    with open(os.path.join(specDir, 'windows-folder-pre-cef.spec'), 'w+', encoding='utf-8') as f:
        f.write(specFirstPart() + specUnpackagePartEXE())
