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

from ac_api._database import DataManager
from ac_api._global import get_scheduler
from ac_api._request import AcRequest


class AcApi:
    def __init__(self, id_, app_):
        self.__id = id_
        self.__app = app_
        self.__scheduler = get_scheduler()
        self.__scheduler_jobs = {}

    request = AcRequest

    def data_manager(self, key):
        return DataManager(key, collection=self.__id)

    def add_cron_job(self, key, func, args=None, kwargs=None, **other_args):
        """

        :param key:
        :param func:
        :param args:
        :param kwargs:
        :param year:
        :param month:
        :param day:
        :param week:
        :param day_of_week:
        :param hour:
        :param minute:
        :param second:
        :param start_date:
        :param end_date:
        :return:
        """
        job = self.__scheduler.add_job(func, trigger='cron', args=[self.__app] + (args or []), kwargs=kwargs,
                                       id=self.__id + key, **other_args)
        self.__scheduler_jobs[job.id] = job

    def edit_cron_job(self, key, **other_args):
        self.__scheduler.reschedule_job(job_id=self.__id + key, trigger='cron', **other_args)
