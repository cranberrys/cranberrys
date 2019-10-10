import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class IndexView(View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return {
            'name': 'AutoCheckIn',
            'main_menu': [
                {
                    'icon': '',
                    'title': '签到中心',
                    'link': 'welcome',
                    'sub_menu': [
                        {
                            'icon': '',
                            'title': '签到中心1',
                            'link': 'auto_check_in',
                        },
                        {
                            'icon': '',
                            'title': '签到中心2',
                            'link': 'welcome2',
                        }
                    ]
                },
                {
                    'icon': '',
                    'title': '签到管理',
                    'link': 'welcome3',
                    'sub_menu': [

                    ]
                }
            ]
        }
