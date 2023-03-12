#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2023-03-12 22:06:45
Description: 数据库类
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 sqlalchemy 模块。
'''

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pyapp.config.config import Config


class DB:
    '''数据库操作类'''

    session = None

    def connect(self):
        '''数据库连接'''
        dbPath = os.path.join(Config.staticDir, 'db', 'base.db')
        print('dbPath', dbPath)
        engine = create_engine(f'sqlite:///{dbPath}?check_same_thread=False', echo=Config.devEnv)
        Session = sessionmaker(bind=engine)
        DB.session = Session()

    def close(self):
        '''关闭数据库连接'''
        if DB.session is not None:
            DB.session.close()
