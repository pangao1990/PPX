#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-03-12 20:08:30
LastEditTime: 2025-06-24 11:07:03
Description: 数据库类 - TinyDB
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 tinydb, cryptography 模块。
'''

import json
import os
from shutil import copyfile

from cryptography.fernet import Fernet
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from api.db.json.models import Models
from pyapp.config.config import Config


class DB:
    '''数据库操作类'''

    dbPath = ''    # 数据库路径

    def init(self):
        '''初始化数据库'''
        # 如果没有数据库，则新建数据库
        dbStaticPath = os.path.join(Config.staticDir, 'db', 'json', 'base.json')    # 程序包
        if not os.path.exists(dbStaticPath):
            # 创建
            with SessionDB(dbStaticPath) as db:
                # 创建一个空的表，名称为 ppx_storage_var
                db.table(Models.PPXStorageVar)

        # 迁移数据库到本地电脑
        dbAppDataDir = os.path.join(Config.appDataDir, 'static', 'db', 'json')    # 本地电脑
        if not os.path.isdir(dbAppDataDir):
            # 新建本地电脑文件夹
            os.makedirs(dbAppDataDir)
        DB.dbPath = os.path.join(dbAppDataDir, 'base.json')    # 本地数据库
        ifCopy = False
        if not os.path.exists(DB.dbPath):
            # 数据库不存在时，新建数据库
            ifCopy = True
        elif Config.ifCoverDB:
            # 配置信息为强制覆盖时，覆盖数据库
            ifCopy = True
        if ifCopy:
            copyfile(dbStaticPath, DB.dbPath)


# 加密数据库
class SessionDB:
    def __init__(self, file_path=None):
        if file_path is None:
            file_path = DB.dbPath
        self.file_path = file_path
        self._db = None
        self.cipher = Fernet(Config.pwDB)    # 密钥

    def _encrypt(self, data):
        return self.cipher.encrypt(json.dumps(data).encode())

    def _decrypt(self, data):
        return json.loads(self.cipher.decrypt(data).decode())

    def __enter__(self):
        try:
            with open(self.file_path, 'rb') as f:
                encrypted_data = f.read()
                data = self._decrypt(encrypted_data)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        self._db = TinyDB(storage=MemoryStorage)
        self._db.storage.write(data)
        return self._db

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._db is not None:
            data = self._db.storage.read()
            with open(self.file_path, 'wb') as f:
                f.write(self._encrypt(data))
        return False
