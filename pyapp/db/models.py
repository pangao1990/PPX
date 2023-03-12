#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /vue-pywebview-pyinstaller的副本/pyapp/db/models.py
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:29:49
LastEditTime: 2023-03-12 22:24:07
Description: 创建数据表
usage: 更新数据表格式后，请按如下操作：
        1、生成迁移文件
            alembic revision --autogenerate -m "在此备注更改内容"
        2、将更改内容更新到数据库
            alembic upgrade head
        3、如有更多需求，请查看文件 pyapp/db/alembic/README
'''

import json

from sqlalchemy import DateTime, Numeric, Column, Integer, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BaseModel(Base):
    '''基类'''
    __abstract__ = True

    def _gen_tuple(self):
        # 处理 日期 等无法正常序列化的对象
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""
        for col in self.__table__.columns:
            try:
                if isinstance(col.type, DateTime):
                    value = convert_datetime(getattr(self, col.name))
                elif isinstance(col.type, Numeric):
                    value = float(getattr(self, col.name))
                else:
                    value = getattr(self, col.name)
                yield (col.name, value)
            except Exception as e:
                print(e)
                pass

    def toDict(self):
        # 转化为 字典
        return dict(self._gen_tuple())

    def toJson(self):
        # 序列化为 JSON
        return json.dumps(self.toDict())


class StorageVar(BaseModel):
    '''储存变量'''
    __tablename__ = "storage_var"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(), doc='键', nullable=False, index=True)
    value = Column(String(), doc='值', server_default='', nullable=False)
    created_at = Column(DateTime(), doc='创建时间', comment='创建时间', server_default=func.now())
    updated_at = Column(DateTime(), doc='更新时间', comment='更新时间', server_default=func.now(), onupdate=func.now())

    def __str__(self):
        return self.key + ' => ' + self.value
