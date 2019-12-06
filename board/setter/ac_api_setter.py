from apscheduler.schedulers.base import STATE_RUNNING

from ac_api._global import get_scheduler


def ac_api_set(app):
    scheduler = get_scheduler()
    if scheduler.state != STATE_RUNNING:
        scheduler.start()
    app['scheduler'] = scheduler
