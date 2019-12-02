#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/11 13:47 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCommand
@FileName: __init__.py
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import json
import time
import uuid
from datetime import datetime
from json import JSONDecodeError

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template

from .everphoto_api import TaskManager


@template('task_add.jinja2')
async def ec_task_add(request):
    return


async def ec_task_action(request):
    data = await request.post()
    task_id = data.get('task_id', '')
    if not task_id:
        return web.json_response({'code': -1, 'msg': '请求参数错误', })
    with request.app['api'].data_manager('task_list') as task_list:
        if task_id not in task_list:
            return web.json_response({'code': -1, 'msg': '找不到任务', })
        task = task_list[task_id]
        if 'token' not in task or task['token'] is None:
            return web.json_response({'code': -1, 'msg': '找不到用户令牌', })
        task_manager = TaskManager(task)

        if task_manager.is_today_checkin:
            return web.json_response({'code': -1, 'msg': '今日已签到', })

        resp_query = await request.app['ec_api'].checkin_query(task['token'])
        if resp_query['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp_query['message'], })
        resp_query_data = resp_query.get('data', {})
        if 'can_checkin' not in resp_query_data:
            return web.json_response({'code': -1, 'msg': '签到状态查询失败', })

        resp_post = await request.app['ec_api'].checkin_post(task['token'])
        if resp_post['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp_post['message'], })

        task_manager.update(resp_post.get('data', {}))

        if resp_query_data['can_checkin'] is False:
            task['last_time'] = datetime.now()
            return web.json_response({'code': -1, 'msg': '今日已通过其他渠道签到', })

    return web.json_response({'code': 0, 'msg': '签到成功', })


async def ec_task_smscode(request):
    data = await request.post()
    mobile = data.get('mobile', '')

    if mobile[0] != '+':
        mobile = '+86' + mobile

    resp = await request.app['ec_api'].smscode(mobile)
    if resp['code'] != 0:
        return web.json_response({'code': -1, 'msg': resp['message'], })
    return web.json_response({'code': 0, 'msg': '发送成功'})


class ECView(View):
    @template('task_list.jinja2')
    async def get(self):
        with self.request.app['api'].data_manager('task_list') as task_list:
            for task in task_list.values():
                last_time = task.get('last_time', '')
                if not last_time or int(time.time() / (60 * 60 * 24)) - int(last_time.timestamp() / (60 * 60 * 24)) > 0:
                    task['can_check_in'] = True
            context = {
                'task_list': task_list.values(),
            }
        return context

    async def post(self):
        data = await self.request.post()
        mobile = data.get('mobile', '')
        smscode = data.get('smscode', '')

        if mobile[0] != '+':
            mobile = '+86' + mobile

        resp = await self.request.app['ec_api'].login(mobile, smscode)
        if resp['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp['message'], })
        resp_data = resp.get('data', {})

        task_id = str(uuid.uuid4())
        with self.request.app['api'].data_manager('task_list') as task_list:
            task_list[task_id] = {
                'id': task_id,
                'mobile': mobile,
                'token': resp_data['token'],
                'last_time': None,
                'last_reward': 0,
                'continuity': 0,
                'total_reward': 0,
                'can_check_in': True,
            }
        return web.json_response({'code': 0, 'msg': '添加成功', })

    async def put(self):
        return

    async def delete(self):
        task_id = self.request.match_info.get('id', '')
        with self.request.app['api'].data_manager('task_list') as task_list:
            if task_id not in task_list:
                return web.json_response({'code': -1, 'msg': '找不到任务', })
            task = task_list.pop(task_id)
        return web.json_response({'code': 0, 'msg': '删除成功', })


class ConfigView(View):
    @template('config.jinja2')
    async def get(self):
        with self.request.app['api'].data_manager('cron_job') as cron_job:
            edit_job = cron_job
        context = {'config': json.dumps(edit_job)}
        return context

    async def post(self):
        data = await self.request.post()
        config_data = data.get('config', '')
        if not config_data:
            return web.json_response({'code': -1, 'msg': '配置为空', })
        try:
            edit_job = json.loads(config_data)
        except JSONDecodeError:
            return web.json_response({'code': -1, 'msg': '配置格式有误', })
        self.request.app['api'].edit_cron_job(key='auto_check_in', **edit_job)
        with self.request.app['api'].data_manager('cron_job') as cron_job:
            cron_job.clear()
            cron_job.update(edit_job)
        return web.json_response({'code': 0, 'msg': '保存成功', })
