from ac_api._global import get_scheduler


def ac_api_set(app):
    scheduler = get_scheduler()
    app['scheduler'] = scheduler
