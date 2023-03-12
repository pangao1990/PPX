#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2023-03-12 21:43:48
Description: 操作数据库类
usage:
    from pyapp.db.orm import ORM

    orm = ORM()    # 操作数据库类
    author = self.orm.getStorageVar('author')    # 获取储存变量
    print('author', author)
'''

from pyapp.db.models import StorageVar
from pyapp.db.db import DB
from sqlalchemy import select


class ORM:
    '''操作数据库类'''

    session = None

    def getStorageVar(self, key):
        '''获取储存变量'''
        resVal = None
        with DB.session.begin():
            stmt = select(StorageVar.value).where(StorageVar.key == key)
            result = DB.session.execute(stmt)
            result = result.one_or_none()
            resVal = result[0]
        return resVal
