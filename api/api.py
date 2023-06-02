#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2023-05-30 15:41:05
Description: 业务层API，供前端JS调用
usage: 在Javascript中调用window.pywebview.api.<methodname>(<parameters>)
'''

from api.storage import Storage
from api.system import System


class API(System, Storage):
    '''业务层API，供前端JS调用'''

    def setWindow(self, window):
        '''获取窗口实例'''
        System.window = window
