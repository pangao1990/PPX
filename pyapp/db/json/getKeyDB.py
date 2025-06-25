#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2025-06-18 17:11:35
LastEditTime: 2025-06-25 10:52:19
Description: 生成 数据库密码
'''

from pathlib import Path

from cryptography.fernet import Fernet


class GetKeyDB:
    '''生成 数据库密码'''

    def getkey(self):
        '''生成 数据库密码'''
        return Fernet.generate_key()

    def run(self):
        '''写入 pyapp/config/config.py'''
        configPath = Path(Path(__file__).absolute().parent.parent.parent.joinpath('config', 'config.py'))
        configContent = ''
        with open(configPath, 'r', encoding='UTF-8') as f:
            configContent = f.read()

        # 写入 pwDB
        if (configContent.find("pwDB = b''") > -1):
            configContent = configContent.replace("pwDB = b''", f"pwDB = {self.getkey()}")

            with open(configPath, 'w', encoding='UTF-8') as f:
                f.write(configContent)

            # 删除旧的数据库
            dbPath = Path(Path(__file__).absolute().parent.parent.parent.parent.joinpath('static', 'db', 'json', 'base.json'))
            if dbPath.exists():
                dbPath.unlink()


if __name__ == '__main__':
    GetKeyDB().run()
