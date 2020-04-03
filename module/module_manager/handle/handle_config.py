#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/5 13:51 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : auto_command
@FileName: handle_config
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import asyncio

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template


class ConfigView(View):
    @template('config.jinja2')
    async def get(self):
        board = self.request.app['board']
        module_list = []
        for module in board.module_all.values():
            if module.name == 'module_manager':
                continue
            module_list.append(module)
        return {'module_list': module_list}

    async def post(self):
        board = self.request.app['board']
        data = await self.request.post()
        action = data.get('action', '')
        module_name = data.get('module_name', '')
        if action == 'start':
            callback = board.enable_module
        elif action == 'stop':
            callback = board.disable_module
        else:
            return web.json_response({'code': -1, 'msg': '请求参数错误', })
        loop = asyncio.get_event_loop()
        loop.call_soon(callback, module_name)
        return web.json_response({'code': 0, 'msg': '插件加载成功，重启后生效', })
