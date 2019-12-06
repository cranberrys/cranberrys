import os

import aiohttp_jinja2
import jinja2
from aiohttp import web

from module.everphoto_checkin.handle.everphoto_api import EverPhoto
from .handle.handle_task import ECView, ec_task_action, ec_task_add, ec_task_smscode, ConfigView
from .handle.scheduler import auto_check_in


async def init(app):
    app['ec_api'] = EverPhoto(app['board_api'].request)
    with app['board_api'].data_manager('cron_job') as cron_job:
        if not cron_job:
            cron_job.update({'hour': '21,23', 'minute': '0'})
        # cron_job.clear()
        # cron_job.update({'minute': '*/1', 'second': '0'})
        app['board_api'].add_cron_job(key='auto_check_in', func=auto_check_in, **cron_job)


def everphoto_checkin():
    app = web.Application()

    module_path = os.path.dirname(os.path.abspath(__file__))
    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(module_path + '/template'))

    app.router.add_view('/task', ECView, name='index')
    app.router.add_view('/config', ConfigView, name='config')
    app.router.add_get('/add', ec_task_add, name='ec_task_add')
    app.router.add_post('/action', ec_task_action, name='ec_task_action')
    app.router.add_post('/smscode', ec_task_smscode, name='ec_task_smscode')
    app.router.add_view('/task/{id}', ECView, name='ec_task_item')

    app.on_startup.append(init)
    return app


if __name__ == '__main__':
    web.run_app(everphoto_checkin())
