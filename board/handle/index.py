import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class IndexView(View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        sub_menu = []
        for module in self.request.app['module_all'].values():
            if not module['loaded']:
                continue
            lib = module['lib']
            sub_menu.append({
                'icon': '',
                'title': lib.title,
                'link': lib.app.router['ec_task_list'].url_for(),
            })

        return {
            'name': 'AutoCheckIn',
            'main_menu': [
                {
                    'icon': '',
                    'title': '签到中心',
                    'sub_menu': sub_menu + [
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
