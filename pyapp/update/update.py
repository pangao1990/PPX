#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
FilePath: /PPX/pyapp/update/update.py
Author: 潘高
LastEditors: 潘高
Date: 2023-03-23 21:24:30
LastEditTime: 2023-06-01 15:55:30
Description: 应用更新
usage: 运行前，请确保本机已经搭建Python3开发环境，且已经安装 httpx 模块。
        详细教程请移步至 https://blog.pangao.vip/Python环境搭建及模块安装/
'''

import os
import subprocess

import httpx

from pyapp.config.config import Config


class AppUpdate:
    '''程序升级'''

    cancelDownload = False    # 是否取消下载

    def check(self):
        '''检查是否有更新：0=>有新版本; -1=>联网失败; 1=>已经是最新版本'''
        resNewInfo = self.__getNewInfo()
        if not resNewInfo['status']:
            # 联网失败
            return {'code': -1, 'msg': '连接服务器失败，请稍后再试'}
        else:
            oldVersion = Config.appVersion
            newVersion = resNewInfo['version']
            ifUpdate = self.__compareVersion(oldVersion, newVersion)    # 判断是否需要更新
            if not ifUpdate:
                # 已是最新版本
                return {'code': 1, 'msg': f'{oldVersion}已是最新版本'}
            else:
                return {'code': 0, 'msg': f'有新版{newVersion}可供更新，当前版本为{oldVersion}。', 'htmlUrl': resNewInfo['htmlUrl'], 'assets': resNewInfo['assets'], 'body': resNewInfo['body']}

    def run(self):
        '''执行更新：0=>下载程序包成功; -1=>联网失败; -2=>下载程序包失败; 1=>已经是最新版本'''
        resCheck = self.check()
        if resCheck['code'] == 0:
            resApp = self.__getApp(resCheck['assets'])
            if not resApp['status']:
                return {'code': -2, 'msg': '下载程序包失败: ' + resApp['msg']}
            else:
                return {'code': 0, 'msg': '下载程序包成功', 'downloadPath': resApp['downloadPath']}
        else:
            return resCheck

    def cancel(self):
        '''取消下载'''
        AppUpdate.cancelDownload = True

    def __getNewInfo(self):
        '''获取服务端版本信息'''
        try:
            # 3秒后连接超时，3秒后读取超时
            r = httpx.get(Config.appUpdateUrl, timeout=(3, 3))
            resJson = r.json()
            version = resJson['name']    # 版本号
            htmlUrl = resJson['html_url']    # 下载页面
            assets = resJson['assets']    # 下载资源
            body = resJson['body']    # 版本介绍
            return {
                'status': True,
                'version': version,
                'htmlUrl': htmlUrl,
                'assets': assets,
                'body': body
            }
        except Exception as e:
            return {
                'status': False,
                'msg': str(e)
            }

    def __compareVersion(self, oldVersion, newVersion):
        '''判断是否需要更新'''
        ifUpdate = False    # 判断是否需要更新
        oldVersionList = oldVersion.replace('V', '').split('.')
        newVersionList = newVersion.replace('V', '').split('.')
        if newVersionList[0] > oldVersionList[0]:
            ifUpdate = True
        elif newVersionList[0] == oldVersionList[0]:
            if newVersionList[1] > oldVersionList[1]:
                ifUpdate = True
            elif newVersionList[1] == oldVersionList[1]:
                if newVersionList[2] > oldVersionList[2]:
                    ifUpdate = True
        return ifUpdate

    def __getApp(self, assetsList):
        '''获取程序包'''
        # 判断更新哪个系统版本
        appExt = '.exe'
        if Config.appIsMacOS:
            appExt = '.dmg'
        for assets in assetsList:
            name = assets['name']
            ext = os.path.splitext(name)[-1]
            if ext == appExt:
                size = assets['size']
                url = assets['browser_download_url']
                downloadPath = os.path.join(Config.downloadDir, name)
                # 超时重连3次
                timeoutCount = 0
                while timeoutCount < 3:
                    resDownload = self.__download(url, downloadPath, size)
                    if resDownload['msg'] == '连接超时':
                        timeoutCount += 1
                    else:
                        return resDownload

    def __download(self, url, downloadPath, size):
        '''下载大文件'''
        from api.api import API
        api = API()
        AppUpdate.cancelDownload = False
        try:
            with open(downloadPath, "wb") as f:
                with httpx.Client(follow_redirects=True) as client:
                    with client.stream("GET", url, timeout=(5, 3600)) as r:
                        downloadSize = 0
                        infoPy2jsDict = dict()
                        # 每块 1KB
                        for chunk in r.iter_bytes(chunk_size=1024):
                            if AppUpdate.cancelDownload:
                                # 取消下载
                                return {'status': False, 'msg': '取消更新'}
                            if chunk:
                                f.write(chunk)
                                f.flush()
                            downloadSize += 1024
                            infoPy2jsDict['sizeShow'] = self.bytes2Size(downloadSize) + ' / ' + self.bytes2Size(size)
                            infoPy2jsDict['percentage'] = int(downloadSize / size * 100)
                            api.system_py2js('py2js_updateAppProgress', infoPy2jsDict)
            return {'status': True, 'msg': '下载成功', 'downloadPath': downloadPath}
        except httpx.TimeoutException:
            # print('TimeoutException => ', '超时')
            return {'status': False, 'msg': '连接超时'}
        except httpx.NetworkError:
            # print('NetworkError => ', '联网失败')
            return {'status': False, 'msg': '联网失败'}
        except httpx.HTTPError as e:
            # print('HTTPError => ', e)
            return {'status': False, 'msg': e}
        except Exception as e:
            # print('Exception => ', e)
            return {'status': False, 'msg': e}

    def bytes2Size(self, bytes):
        '''将字节大小转为带单位的值'''
        if bytes < 1024:    # 比特
            bytes = str(round(bytes, 0)) + ' B'    # 字节
        elif bytes >= 1024 and bytes < 1024 * 1024:
            bytes = str(round(bytes / 1024, 0)) + ' KB'    # 千字节
        elif bytes >= 1024 * 1024 and bytes < 1024 * 1024 * 1024:
            bytes = str(round(bytes / 1024 / 1024, 1)) + ' MB'    # 兆字节
        elif bytes >= 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024:
            bytes = str(round(bytes / 1024 / 1024 / 1024, 2)) + ' GB'    # 千兆字节
        elif bytes >= 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024:
            bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024, 2)) + ' TB'    # 太字节
        elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
            bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' PB'    # 拍字节
        elif bytes >= 1024 * 1024 * 1024 * 1024 * 1024 * 1024 and bytes < 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024:
            bytes = str(round(bytes / 1024 / 1024 / 1024 / 1024 / 1024 / 1024, 2)) + ' EB'    # 艾字节
        return bytes

    def IfMacAppleM(self):
        '''判断是苹果M芯片还是Intel芯片'''
        p = subprocess.Popen('sysctl machdep.cpu.brand_string', shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        res = out.decode('UTF-8')
        if res.find('Apple M') > -1:
            return True
        else:
            return False
