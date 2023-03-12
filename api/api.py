#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2022-03-21 17:01:39
LastEditTime: 2023-03-12 21:44:44
Description: 本地API，供前端JS调用
usage: 调用window.pywebview.api.<methodname>(<parameters>)从Javascript执行
'''

import getpass
import json
import os
from pyapp.db.orm import ORM
import webview


class API:
    '''本地API，供前端JS调用'''

    window = None

    orm = ORM()    # 操作数据库类

    def getOwner(self):
        # 调用js挂载的函数，返回结果可在控制台查看
        self.py2js({'tip': '来自py的调用'})

        # 获取数据库的值
        author = self.orm.getStorageVar('author')
        print('author', author)    # python打印结果可在终端查看

        return getpass.getuser()

    def py2js(self, info):
        '''调用js中挂载到window的函数'''
        infoJson = json.dumps(info)
        API.window.evaluate_js(f"py2js('{infoJson}')")

    def pyCreateFileDialog(self, fileTypes=['全部文件 (*.*)'], directory=''):
        '''打开文件对话框'''
        # 可选文件类型
        # fileTypes = ['Excel表格 (*.xlsx;*.xls)']
        fileTypes = tuple(fileTypes)    # 要求必须是元组
        result = API.window.create_file_dialog(dialog_type=webview.OPEN_DIALOG, directory=directory, allow_multiple=True, file_types=fileTypes)
        resList = list()
        if result is not None:
            for res in result:
                filePathList = os.path.split(res)
                dir = filePathList[0]
                filename = filePathList[1]
                ext = os.path.splitext(res)[-1]
                resList.append({
                    'filename': filename,
                    'ext': ext,
                    'dir': dir,
                    'path': res
                })
        return resList
