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
from ac_api._cronjob import CronJob
from ac_api._database import DataManager
from ac_api._request import AcRequest
from ac_api._global import get_new_scheduler


class AcApi:
    cron_job_reset = get_new_scheduler

    def __init__(self, name, module):
        self.__name = name
        self.__module = module

        self.request = AcRequest
        self.cron_job = CronJob(name=self.__name, module=self.__module)

    def data_manager(self, key):
        return DataManager(key, collection=self.__name)
