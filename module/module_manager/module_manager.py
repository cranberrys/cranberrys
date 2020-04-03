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

from ac_api import AcApplication
from .handle.handle_config import ConfigView


async def init_callback(app):
    pass


def module_manager():
    static_path = os.path.dirname(os.path.abspath(__file__)) + '/template'

    app = AcApplication()
    app.ac_set_static_path(static_path)
    app.router.add_view('/config', ConfigView, name='config')
    app.ac_set_init_callback(init_callback)

    return app


if __name__ == '__main__':
    module_manager().run()
