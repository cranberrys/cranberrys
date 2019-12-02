import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class IndexView(View):
    @aiohttp_jinja2.template('index.jinja2')
    async def get(self):
        sub_index, sub_config = [], []
        for module in self.request.app['module_all'].values():
            if not module['loaded']:
                continue
            lib = module['lib']
            if lib.plug_info['index']:
                sub_index.append({
                    'icon': '',
                    'title': lib.plug_info['title'],
                    'link': lib.plug_info['index'].url_for(),
                })
            if lib.plug_info['config']:
                sub_config.append({
                    'icon': '',
                    'title': lib.plug_info['title'] + '设置',
                    'link': lib.plug_info['config'].url_for(),
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
