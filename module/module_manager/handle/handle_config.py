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

from ac_api import AcResponse, AcView, ac_template, AcAsync


class ConfigView(AcView):
    @ac_template('config.jinja2')
    async def get(self):
        module_list = []
        for module in self.board.module_all.values():
            if module.name == 'module_manager':
                continue
            module_list.append(module)
        return {'module_list': module_list}

    async def post(self):
        data = await self.request.post()
        action = data.get('action', '')
        module_name = data.get('module_name', '')
        if action == 'start':
            callback = self.board.enable_module
        elif action == 'stop':
            callback = self.board.disable_module
        else:
            return AcResponse.json({'code': -1, 'msg': '请求参数错误', })
        AcAsync.call_soon(callback, module_name)
        return AcResponse.json({'code': 0, 'msg': '插件加载成功，重启后生效', })
