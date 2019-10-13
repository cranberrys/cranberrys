import aiohttp_jinja2
from aiohttp.web_urldispatcher import View

from module.everphoto_checkin import app


class IndexView(View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        return {
            'name': 'AutoCheckIn',
            'main_menu': [
                {
                    'icon': '',
                    'title': '签到中心',
                    'sub_menu': [
                        {
                            'icon': '',
                            'title': '时光相册',
                            'link': app.router['ec_task_list'].url_for(),
                        },
                        {
                            'icon': '',
                            'title': '敬请期待',
                            'link': 'welcome',
                        }
                    ]
                },
                {
                    'icon': '',
                    'title': '签到管理',
                    'sub_menu': [

                    ]
                }
            ]
        }
