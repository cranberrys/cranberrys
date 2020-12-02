#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/11 13:48 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCommand
@FileName: __init__.py
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import asyncio
import logging
import pathlib

import aiohttp_jinja2
import jinja2
from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template

from ac_api._cronjob import CronJob
from ac_api._database import DataManager
from ac_api._global import get_new_scheduler
from ac_api._request import AcRequest

AcCronJobReset = get_new_scheduler

ac_template = template


class AcApplication(web.Application):
    _module = None
    _name = None

    board = None
    cron_job = None
    request = AcRequest

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(static_path))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self.cron_job = CronJob(name=self.name, module=self)

    @property
    def module(self):
        return self._module

    @module.setter
    def module(self, value):
        self._module = value
        self.name = self.module.name

    def data_manager(self, key):
        return DataManager(key, collection=self.name)

    def ac_set_template_path(self, path):
        template_path = pathlib.Path(self.module.path) / path
        if template_path.exists():
            aiohttp_jinja2.setup(self, loader=jinja2.FileSystemLoader(template_path))
        else:
            logging.warning(f'template path {template_path} not exists')

    def ac_set_static_path(self, path):
        static_path = pathlib.Path(self.module.path) / path
        if static_path.exists():
            self.router.add_static('/static', static_path)
        else:
            logging.warning(f'static path {static_path} not exists')

    def ac_set_init_callback(self, callback):
        self.on_startup.append(callback)

    def run(self):
        web.run_app(self)


class AcAsync:
    call_soon = lambda callback, *args: asyncio.get_event_loop().call_soon(callback, *args)


class AcResponse:
    json = web.json_response


class AcResponseErr:
    redirect = web.HTTPFound


class AcView(View):
    @property
    def app(self):
        return self.request.app

    @property
    def board(self):
        return self.app.board
