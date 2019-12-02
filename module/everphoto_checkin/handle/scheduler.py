import logging

from .everphoto_api import TaskManager


async def check_in(api, task):
    task_manager = TaskManager(task)
    # 上次签到时间为今天则跳过
    if task_manager.is_today_checkin:
        return logging.info(f'task {task["id"]} today already checkin')

    # 查询任务失败跳过
    resp = await api.checkin_query(task["token"])
    if resp['code'] != 0:
        return logging.error(f'task {task["id"]} query fail', resp)

    # 签到失败跳过
    resp = await api.checkin_post(task['token'])
    if resp['code'] != 0:
        return logging.error(f'task {task["id"]} checkin fail', resp)

    logging.info(f'task {task["id"]} checkin success')
    task_manager.update(resp.get('data', {}))


async def auto_check_in(app):
    logging.info('scheduler start')
    with app['api'].data_manager('task_list') as task_list:
        for task in task_list.values():
            try:
                await check_in(app['ec_api'], task)
            except Exception as err:
                logging.exception(err)
    logging.info('scheduler over')
