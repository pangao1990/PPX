#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2025-06-24 09:29:27
Description: 操作数据库类
usage:
    from api.db.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
'''

from pyapp.config.config import Config


class ORM:
    '''数据库操作类'''

    def __init__(self, *args, **kwargs):
        if Config.typeDB == 'sql':
            from api.db.sql.orm import ORM as sqlORM
            self._impl = sqlORM(*args, **kwargs)
        else:
            from api.db.json.orm import ORM as jsonORM
            self._impl = jsonORM(*args, **kwargs)

    def __getattr__(self, name):
        '''将属性访问委托给具体的数据库实现类'''
        return getattr(self._impl, name)