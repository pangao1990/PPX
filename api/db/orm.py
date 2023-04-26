#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2023-04-12 20:50:53
Description: 操作数据库类
usage:
    from api.db.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
'''

from api.db.models import PPXStorageVar
from pyapp.db.db import DB
from sqlalchemy import select, update, insert


class ORM:
    '''操作数据库类'''

    def getStorageVar(self, key):
        '''获取储存变量'''
        resVal = ''
        dbSession = DB.session()
        with dbSession.begin():
            stmt = select(PPXStorageVar.value).where(PPXStorageVar.key == key)
            result = dbSession.execute(stmt)
            result = result.one_or_none()
            if result is None:
                # 新建
                stmt = insert(PPXStorageVar).values(key=key)
                dbSession.execute(stmt)
            else:
                resVal = result[0]
        dbSession.close()
        return resVal

    def setStorageVar(self, key, val):
        '''更新储存变量'''
        dbSession = DB.session()
        with dbSession.begin():
            stmt = update(PPXStorageVar).where(PPXStorageVar.key == key).values(value=val)
            dbSession.execute(stmt)
        dbSession.close()
