import time
from datetime import datetime

from ac_api.database import data_manager
from .everphoto_api import EverPhoto


async def auto_check_in():
    print('scheduler start')

    with data_manager('task_list', collection='everphoto_checkin') as task_list:
        for task in task_list.values():
            # 上次签到时间为今天则跳过
            last_time = task.get('last_time', '')
            if last_time and int(time.time() / (60 * 60 * 24)) - int(last_time.timestamp() / (60 * 60 * 24)) == 0:
                print(f'task {task["id"]} today already checkin')
                continue

            # 查询任务失败跳过
            resp = await EverPhoto.checkin_query(task['token'])
            if resp['code'] != 0:
                print(f'task {task["id"]} query fail', resp)
                continue

            # 查询到今日已签到跳过
            resp_data = resp.get('data', {})
            task['can_check_in'] = resp_data['can_checkin']
            if resp_data['can_checkin'] is False:
                task['last_time'] = datetime.now()
                print(f'task {task["id"]} query today already checkin')
                continue

            # 签到失败跳过
            resp = await EverPhoto.checkin_post(task['token'])
            if resp['code'] != 0:
                print(f'task {task["id"]} checkin fail', resp)
                continue

            print(f'task {task["id"]} checkin success')
            resp_data = resp['data']
            if resp_data['checkin_result']:
                task['last_time'] = datetime.now()
                task['last_reward'] = resp_data['reward']  # 签到获得空间奖励 单位 字节
            task['continuity'] = resp_data['continuity']  # 连续签到天数
            task['total_reward'] = resp_data['total_reward']  # 累计签到获得空间奖励 单位 字节
            task['tomorrow_reward'] = resp_data['tomorrow_reward']  # 明天签到获得空间奖励 单位 字节
            task['can_check_in'] = False

    print('scheduler over')
