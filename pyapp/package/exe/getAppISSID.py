#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Author: 潘高
LastEditors: 潘高
Date: 2023-04-25 10:25:55
LastEditTime: 2025-06-18 17:14:01
Description: 生成 appISSID 打包唯一编号。
'''
import random
from pathlib import Path


class GetAPPISSID:
    '''生成 appISSID 打包唯一编号'''

    def getItem(self, k=4):
        '''从0123456789ABCDEF中随机获取k个字符组成一个新的字符串'''
        itemList = random.choices(population="0123456789ABCDEF", k=k)
        return ''.join(itemList)

    def getAppISSID(self):
        '''生成 appISSID 打包唯一编号'''
        return f'{self.getItem(8)}-{self.getItem(4)}-{self.getItem(4)}-{self.getItem(4)}-{self.getItem(12)}'

    def run(self):
        '''写入 pyapp/config/config.py'''
        configPath = Path(Path(__file__).absolute().parent.parent.parent.joinpath('config', 'config.py'))
        configContent = ''
        with open(configPath, 'r', encoding='UTF-8') as f:
            configContent = f.read()

        # 写入 appISSID
        configContent = configContent.replace("appISSID = ''", f"appISSID = '{self.getAppISSID()}'")

        with open(configPath, 'w', encoding='UTF-8') as f:
            f.write(configContent)


if __name__ == '__main__':
    GetAPPISSID().run()
