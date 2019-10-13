from apscheduler.schedulers.asyncio import AsyncIOScheduler


def scheduler_set(app):
    scheduler = AsyncIOScheduler({
        # 'apscheduler.jobstores.mongo': {
        #     'type': 'mongodb'
        # }
    })
    scheduler.start()
    app['scheduler'] =scheduler

    # expiry_job = scheduler.add_job(tasks.expiry, 'cron', hour='0', minute='0,1', args=[app], id='expiry')  # 票券过期处理
    # check_job = scheduler.add_job(tasks.check, 'cron', hour='0', minute='2', args=[app], id='check')  # 票券核验处理
    # notice_job = scheduler.add_job(tasks.notice, 'cron', hour='0', minute='3', args=[app], id='notice')  # 报表通知
    #
    # app['tasks'].update({
    #     'expiry': expiry_job,
    #     'check': check_job,
    #     'notice': notice_job
    # })
