#!/usr/bin/env python
# encoding: utf-8

"""
@Time    : 2020/4/3 10:37
@Author  : Sam Wang
@Email   : muumlover@live.com
@Blog    : https://blog.ronpy.com
@Project : auto_command
@FileName: _cronjob
@Software: PyCharm
@license : (C) Copyright 2019 by Sam Wang. All rights reserved.
@Desc    : 
    
"""
from ._global import get_scheduler


class CronJob:
    def __init__(self, name, module):
        self.__name = name
        self.__module = module
        self.__scheduler_jobs = {}

    @property
    def __scheduler(self):
        return get_scheduler()

    def __get_job_id(self, job_key):
        return self.__name + '__' + job_key

    def add(self, key, func, args=None, kwargs=None, **other_args):
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
        job_id = self.__get_job_id(key)
        old_job = self.__scheduler.get_job(job_id)
        if old_job:
            self.__scheduler.remove_job(job_id)
        job = self.__scheduler.add_job(func, trigger='cron', args=[self.__module] + (args or []), kwargs=kwargs,
                                       id=job_id, **other_args)
        if self.__name not in self.__scheduler_jobs:
            self.__scheduler_jobs[self.__name] = {}
        self.__scheduler_jobs[self.__name][job.id] = job

    def edit(self, key, **other_args):
        self.__scheduler.reschedule_job(job_id=self.__get_job_id(key), trigger='cron', **other_args)

    def stop_all(self):
        for k, v in self.__scheduler_jobs[self.__name].items():
            self.__scheduler.remove_job(v.id)
