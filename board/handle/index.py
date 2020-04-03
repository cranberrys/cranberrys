from ac_api import AcView, ac_template


class IndexView(AcView):
    @ac_template('index.jinja2')
    async def get(self):
        sub_index, sub_config = [], []
        for module in self.app.module_all.values():
            if not module.loaded:
                continue
            if module.app.router.get('index'):
                sub_index.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'],
                    'link': module.app.router.get('index').url_for(),
                })
            if module.app.router.get('config'):
                sub_config.append({
                    'icon': '',
                    'title': module.lib.plug_info['title'] + '设置',
                    'link': module.app.router.get('config').url_for(),
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
