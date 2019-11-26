import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from ac_api.scheduler import scheduler
from .handle.handle_task import ECView, ec_task_action, ec_task_add, ec_task_smscode
from .handle.scheduler import auto_check_in


async def handler(request):
    location = request.app.router['ec_task_list'].url_for()
    raise web.HTTPFound(location=location)


everphoto_checkin = web.Application()

module_path = os.path.dirname(os.path.abspath(__file__))
aiohttp_jinja2.setup(everphoto_checkin, loader=jinja2.FileSystemLoader(module_path + '/template'))

everphoto_checkin.router.add_get('', handler)
everphoto_checkin.router.add_get('/', handler)
everphoto_checkin.router.add_get('/add', ec_task_add, name='ec_task_add')

everphoto_checkin.router.add_post('/action', ec_task_action, name='ec_task_action')
everphoto_checkin.router.add_post('/smscode', ec_task_smscode, name='ec_task_smscode')

everphoto_checkin.router.add_view('/task', ECView, name='ec_task_list')
everphoto_checkin.router.add_view('/task/{id}', ECView, name='ec_task_item')


async def init(app):
    jobs = [
        {'func': auto_check_in, 'trigger': 'cron', 'hour': '21,23', 'minute': '0'}
    ]
    for job in jobs:
        scheduler.add_job(**job)


everphoto_checkin.on_startup.append(init)

if __name__ == '__main__':
    web.run_app(everphoto_checkin)
