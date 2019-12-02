#!/usr/bin/env python3
# encoding: utf-8

"""
@Time    : 2019/10/11 13:33 
@Author  : Sam
@Email   : muumlover@live.com
@Blog    : https://blog.muumlover.com
@Project : AutoCommand
@FileName: everphoto_api
@Software: PyCharm
@license : (C) Copyright 2019 by muumlover. All rights reserved.
@Desc    : 
    
"""
import time
from datetime import datetime

BASE_URL = 'https://api.everphoto.cn'


class TaskManager:
    def __init__(self, task):
        self.task = task

    @property
    def is_today_checkin(self):
        last_time = self.task.get('last_time', '')
        if last_time and int(time.time() / (60 * 60 * 24)) - int(last_time.timestamp() / (60 * 60 * 24)) == 0:
            return True
        return False

    def update(self, data):
        self.task['last_time'] = datetime.now()
        self.task['last_reward'] = data.get('reward', 0)  # 签到获得空间奖励 单位 字节
        self.task['continuity'] = data.get('continuity', 0)  # 连续签到天数
        self.task['total_reward'] = data.get('total_reward', 0)  # 累计签到获得空间奖励 单位 字节
        self.task['tomorrow_reward'] = data.get('tomorrow_reward', 0)  # 明天签到获得空间奖励 单位 字节
        self.task['can_check_in'] = False


class EverPhoto:
    def __init__(self, request_api):
        self._request = request_api

    async def check_mobile(self, mobile, country_code='+86'):
        """
        获取账号状态
        :param mobile: 手机号码 13312345678
        :param country_code: 国家代码 +86
        :return:
        """
        content = await self._request.get(f'{BASE_URL}/auth/mobile/check',
                                          params={'mobile': mobile, 'country_code': country_code})
        return content

    async def smscode(self, mobile):
        """
        获取验证码
        :param mobile: 手机号码 +8613312345678
        :return:
        """
        content = await self._request.get(f'{BASE_URL}/smscode', params={'mobile': mobile})
        return content

    async def login(self, mobile, smscode):
        """
        登录
        :param mobile: 手机号码 +8613312345678
        :param smscode: 验证码 1234
        :return:
        """
        content = await self._request.post(f'{BASE_URL}/auth', data={'mobile': mobile, 'smscode': smscode})
        return content

    async def checkin_post(self, token):
        """
        提交签到
        :param token: 令牌
        :return:
        """
        content = await self._request.post(f'{BASE_URL}/users/self/checkin/v2',
                                           headers={'Authorization': f'Bearer {token}'})
        return content
        # content_data = content.get('data', {})
        # checkin_result = content_data.get('checkin_result', None)  # 签到结果
        # reward = content_data.get('reward', 0)  # 签到获得空间奖励 单位 字节
        # continuity = content_data.get('continuity', 0)  # 连续签到天数
        # total_reward = content_data.get('total_reward', 0)  # 累计签到获得空间奖励 单位 字节
        # tomorrow_reward = content_data.get('tomorrow_reward', 0)  # 明天签到获得空间奖励 单位 字节
        # return checkin_result

    async def checkin_query(self, token):
        """
        查询签到
        {'timestamp': 1570771777, 'code': 20104, 'message': '未登录'}
        {'timestamp': 1570771876, 'code': 0, 'data': {'can_checkin': False, 'reward_rule_title': '签到奖励规则', 'reward_rule_content': '连续签到7天以上每天可得50MB永久空间', 'reward_rule_list': [{'continuity': '第1天', 'reward': '+1MB'}, {'continuity': '第2天', 'reward': '+2MB'}, {'continuity': '第3天', 'reward': '+3MB'}, {'continuity': '第4天', 'reward': '+4MB'}, {'continuity': '第5天', 'reward': '+5MB'}, {'continuity': '第6天', 'reward': '+6MB'}, {'continuity': '第7天', 'reward': '+50MB'}, {'continuity': '第7+天', 'reward': '+50MB'}], 'member_list_title': '赚取更多永久空间', 'member_list_data': [{'level': '成为初级会员', 'privilege': '签到奖励x2'}, {'level': '成为中级会员', 'privilege': '签到奖励x3'}, {'level': '成为高级会员', 'privilege': '签到奖励x4'}]}}

        :param token: 令牌
        :return:
        """
        content = await self._request.get(f'{BASE_URL}/users/self/checkin/v2',
                                          headers={'Authorization': f'Bearer {token}'})
        return content
        # can_checkin = content.get('data', {}).get('can_checkin', None)
        # return can_checkin


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    # loop.run_until_complete(EverPhoto.checkin_query('iN6KIPvlJ-GIXK5wdO7sfDNL'))
    # loop.run_until_complete(EverPhoto.checkin_post('iN6KIPvlJ-GIXK5wdO7sfDNL'))
