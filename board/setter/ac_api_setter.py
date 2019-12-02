from ac_api._global import scheduler


def ac_api_set(app):
    scheduler.start()
    app['scheduler'] = scheduler
