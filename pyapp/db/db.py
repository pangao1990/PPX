#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2025-06-24 08:50:25
LastEditTime: 2025-06-24 09:29:46
Description: 数据库类
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装  模块。
'''

from pyapp.config.config import Config


class DB:
    '''数据库操作类'''

    def __init__(self, *args, **kwargs):
        if Config.typeDB == 'sql':
            from pyapp.db.sql.db import DB as sqlDB
            self._impl = sqlDB(*args, **kwargs)
        else:
            from pyapp.db.json.db import DB as jsonDB
            self._impl = jsonDB(*args, **kwargs)

    def __getattr__(self, name):
        '''将属性访问委托给具体的数据库实现类'''
        return getattr(self._impl, name)