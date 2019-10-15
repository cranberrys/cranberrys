from .app import everphoto_checkin as app
from .handle.scheduler import auto_check_in

title = '时光相册'
name = 'everphoto_checkin'
jobs = [
    # {'func': test, 'trigger': 'cron', 'args': [app], 'hour': '23', 'minute': '0', 'id': 'expiry'}
    # {'func': auto_check_in, 'trigger': 'cron', 'second': '*/5'}
    {'func': auto_check_in, 'trigger': 'cron', 'hour': '23', 'minute': '0'}
]
