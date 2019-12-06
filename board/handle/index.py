import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class IndexView(View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        sub_index, sub_config = [], []
        for module in self.request.app.module_all.values():
            if not module.loaded:
                continue
            if module.lib.app.router.get('index'):
                sub_index.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'],
                    'link': module.lib.app.router.get('index').url_for(),
                })
            if module.lib.app.router.get('config'):
                sub_config.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'] + '设置',
                    'link': module.lib.app.router.get('config').url_for(),
                })

        return {
            'name': 'AutoCommand',
            'main_menu': [
                {
                    'icon': '',
                    'title': '签到中心',
                    'sub_menu': sub_index + [
                        {
                            'icon': '',
                            'title': '敬请期待',
                            'link': 'error',
                        }
                    ]
                },
                {
                    'icon': '',
                    'title': '签到管理',
                    'sub_menu': sub_config + [

                    ]
                }
            ]
        }
