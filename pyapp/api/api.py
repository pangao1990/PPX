#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PyWebView/vue-pywebview-pyinstaller/pyapp/api/api.py
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2022-03-23 15:40:25
Description: 本地API，供前端JS调用
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''

import getpass


class API:
    '''本地API，供前端JS调用'''

    def getOwner(self):
        return getpass.getuser()
