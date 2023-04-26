#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-25 19:39:03
LastEditTime: 2023-03-25 20:11:10
Description: 操作存储在数据库中的数据
usage: 调用window.pywebview.api.storage.<methodname>(<parameters>)从Javascript执行
'''

from api.db.orm import ORM


class Storage:
    '''存储类'''

    orm = ORM()    # 操作数据库类

    def storage_get(self, key):
        '''获取关键词的值'''
        return self.orm.getStorageVar(key)

    def storage_set(self, key, val):
        '''设置关键词的值'''
        self.orm.setStorageVar(key, val)
