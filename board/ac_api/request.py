#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/11 13:34 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCommand
@FileName: request
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import aiohttp


class AcRequest:
    @staticmethod
    async def get(url, params=None, headers=None):
        async with aiohttp.request('GET', url, params=params, headers=headers) as resp:
            content = await resp.json()
        return content

    @staticmethod
    async def post(url, params=None, data=None, json=None, headers=None):
        async with aiohttp.request('POST', url, params=params, data=data, json=json, headers=headers) as resp:
            content = await resp.json()
        return content
