#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/11 13:47 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCheckIn
@FileName: __init__.py
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import render_template

from data_manager import dm


class EverPhotoCheckInView(View):
    async def get(self):
        token = dm.get('token', '')
        context = {'name': token}
        response = render_template('module/everphoto_checkin.jinja2', self.request, context)
        return response

    async def post(self):
        token = dm.get('token', '')
        response = {'name': token}
        return response
