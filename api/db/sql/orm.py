#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2025-06-24 09:20:27
Description: 操作数据库类 - sql
usage:
    from api.db.sql.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
'''

from sqlalchemy import select, update
from sqlalchemy.dialects.sqlite import insert

from api.db.sql.models import PPXStorageVar
from pyapp.db.sql.db import DB


class ORM:
    '''操作数据库类'''

    def getStorageVar(self, key):
        '''获取储存变量'''
        resVal = ''
        dbSession = DB.session()
        with dbSession.begin():
            stmt = select(PPXStorageVar.val).where(PPXStorageVar.key == key)
            result = dbSession.execute(stmt)
            result = result.one_or_none()
            if result is not None:
                resVal = result[0]
        dbSession.close()
        return resVal

    def setStorageVar(self, key, val):
        '''更新储存变量'''
        dbSession = DB.session()
        with dbSession.begin():
            data = {'key': key, 'val': val}
            stmt = insert(PPXStorageVar).values(**data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['key'],  # 唯一索引或主键
                set_=data
            )
            dbSession.execute(stmt)
        dbSession.close()
