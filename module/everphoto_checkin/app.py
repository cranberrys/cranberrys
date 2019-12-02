import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from module.everphoto_checkin.handle.everphoto_api import EverPhoto
from .handle.handle_task import ECView, ec_task_action, ec_task_add, ec_task_smscode, ConfigView
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

everphoto_checkin.router.add_view('/config', ConfigView, name='ec_config')


async def init(app):
    app['ec_api'] = EverPhoto(app['api'].request)
    with app['api'].data_manager('cron_job') as cron_job:
        if not cron_job:
            cron_job.update({'hour': '21,23', 'minute': '0'})
        # cron_job.clear()
        # cron_job.update({'minute': '*/1', 'second': '0'})
        app['api'].add_cron_job(key='auto_check_in', func=auto_check_in, **cron_job)


everphoto_checkin.on_startup.append(init)

if __name__ == '__main__':
    web.run_app(everphoto_checkin)
