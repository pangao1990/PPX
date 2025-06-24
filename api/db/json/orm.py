#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2025-06-24 09:40:21
Description: 操作数据库类 - json
usage:
    from api.db.json.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
'''

from pyapp.db.json.db import SessionDB
from api.db.json.models import Models
from tinydb import Query


class ORM:
    '''操作数据库类'''

    def getStorageVar(self, key):
        '''获取储存变量'''
        resVal = ''
        with SessionDB() as db:
            table = db.table(Models.PPXStorageVar)
            Q = Query()
            results = table.search(Q.key == key)
            if len(results) > 0 and 'val' in results[0]:
                resVal = results[0]['val']
        return resVal

    def setStorageVar(self, key, val):
        '''更新储存变量'''
        with SessionDB() as db:
            data = {'key': key, 'val': val}
            table = db.table(Models.PPXStorageVar)
            Q = Query()
            table.upsert(data, Q.key == key)
