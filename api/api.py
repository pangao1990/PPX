#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2023-04-12 08:50:47
Description: 本地API，供前端JS调用
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''

import getpass
import json

from api.storage import Storage
from api.system import System


class API(System, Storage):
    '''本地API，供前端JS调用'''

    def setWindow(self, window):
        '''获取窗口实例'''
        System.window = window

    def getOwner(self):
        # 调用js挂载的函数，返回结果可在控制台查看
        self.py2js({'tip': '来自py的调用'})

        return getpass.getuser()

    def py2js(self, info):
        '''调用js中挂载到window的函数'''
        infoJson = json.dumps(info)
        API.window.evaluate_js(f"py2js('{infoJson}')")
