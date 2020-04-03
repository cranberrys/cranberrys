#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/11/25 14:18 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : auto_command
@FileName: scheduler
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import STATE_STOPPED

__scheduler = None


def get_scheduler():
    global __scheduler
    if not __scheduler or __scheduler.state == STATE_STOPPED:
        del __scheduler
        __scheduler = AsyncIOScheduler({
            # 'apscheduler.jobstores.mongo': {
            #     'type': 'mongodb'
            # }
        })
        __scheduler.start()
    return __scheduler


def get_new_scheduler():
    global __scheduler
    if __scheduler:
        __scheduler.remove_all_jobs()
    __scheduler = None
    return get_scheduler()
