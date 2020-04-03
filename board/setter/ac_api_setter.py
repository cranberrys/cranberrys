from ac_api import AcCronJobReset


def ac_api_set(app):
    scheduler = AcCronJobReset()
    app['scheduler'] = scheduler
