#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/12/5 13:50 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : auto_command
@FileName: module_manager
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""

import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from .handle.handle_config import ConfigView


async def init(app):
    pass


def module_manager():
    app = web.Application()

    module_path = os.path.dirname(os.path.abspath(__file__))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(module_path + '/template'))

    app.router.add_view('/config', ConfigView, name='config')

    app.on_startup.append(init)
    return app


if __name__ == '__main__':
    web.run_app(module_manager())
