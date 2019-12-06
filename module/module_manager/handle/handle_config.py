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

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template


class ConfigView(View):
    @template('config.jinja2')
    async def get(self):
        board = self.request.app['board']
        plug_enable = []
        plug_disable = []
        for module in board.module_all.values():
            if module.name == 'module_manager':
                continue
            if module.loaded:
                plug_enable.append(module.lib.plug_info)
            else:
                plug_disable.append(module)
        return {'plug_enable': plug_enable, 'plug_disable': plug_disable}

    async def post(self):
        board = self.request.app['board']
        data = await self.request.post()
        action = data.get('action', '')
        plug_name = data.get('plug_name', '')
        board.enable_module(plug_name)
        return web.json_response({'code': 0, 'msg': '插件加载成功，重启后生效', })
