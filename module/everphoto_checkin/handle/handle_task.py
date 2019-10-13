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
import time
import uuid
from datetime import datetime

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_jinja2 import template

from board.ac_api.database import data_manager
from .everphoto_api import EverPhoto


@template('task_add.jinja2')
async def ec_task_add(request):
    return


async def ec_task_action(request):
    data = await request.post()
    task_id = data.get('task_id', '')
    if not task_id:
        return web.json_response({'code': -1, 'msg': '请求参数错误', })
    with data_manager('task_list', 'everphoto_checkin') as task_list:
        if task_id not in task_list:
            return web.json_response({'code': -1, 'msg': '找不到任务', })
        task = task_list[task_id]
        if 'token' not in task or task['token'] is None:
            return web.json_response({'code': -1, 'msg': '找不到用户令牌', })

        last_time = task.get('last_time', '')
        if last_time and int(time.time() / (60 * 60 * 24)) - int(last_time.timestamp() / (60 * 60 * 24)) == 0:
            return web.json_response({'code': -1, 'msg': '今日已签到', })

        resp = await EverPhoto.checkin_query(task['token'])
        if resp['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp['message'], })
        resp_data = resp.get('data', {})
        if 'can_checkin' not in resp_data:
            return web.json_response({'code': -1, 'msg': '签到状态查询失败', })
        task['can_check_in'] = resp_data['can_checkin']
        if resp_data['can_checkin'] is False:
            task['last_time'] = datetime.now()
            return web.json_response({'code': -1, 'msg': '今日已签到', })

        resp = await EverPhoto.checkin_post(task['token'])
        if resp['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp['message'], })
        resp_data = resp.get('data', {})
        task['last_time'] = datetime.now()
        task['last_reward'] = resp_data.get('reward', 0)  # 签到获得空间奖励 单位 字节
        task['continuity'] = resp_data.get('continuity', 0)  # 连续签到天数
        task['total_reward'] = resp_data.get('total_reward', 0)  # 累计签到获得空间奖励 单位 字节
        task['tomorrow_reward'] = resp_data.get('tomorrow_reward', 0)  # 明天签到获得空间奖励 单位 字节
        task['can_check_in'] = False

    return web.json_response({'code': 0, 'msg': '签到成功', })


async def ec_task_smscode(request):
    data = await request.post()
    mobile = data.get('mobile', '')

    if mobile[0] != '+':
        mobile = '+86' + mobile

    resp = await EverPhoto.smscode(mobile)
    if resp['code'] != 0:
        return web.json_response({'code': -1, 'msg': resp['message'], })
    return web.json_response({'code': 0, 'msg': '发送成功'})


class ECView(View):
    @template('task_list.jinja2')
    async def get(self):
        with data_manager('task_list', 'everphoto_checkin') as task_list:
            for task in task_list.values():
                last_time = task.get('last_time', '')
                if last_time and int(time.time() / (60 * 60 * 24)) - int(last_time.timestamp() / (60 * 60 * 24)) > 0:
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

        resp = await EverPhoto.login(mobile, smscode)
        if resp['code'] != 0:
            return web.json_response({'code': -1, 'msg': resp['message'], })
        resp_data = resp.get('data', {})

        task_id = str(uuid.uuid4())
        with data_manager('task_list', 'everphoto_checkin') as task_list:
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
        with data_manager('task_list', 'everphoto_checkin') as task_list:
            if task_id not in task_list:
                return web.json_response({'code': -1, 'msg': '找不到任务', })
            task = task_list.pop(task_id)
        return web.json_response({'code': 0, 'msg': '删除成功', })
