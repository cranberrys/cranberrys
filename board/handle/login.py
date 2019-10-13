import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class LoginView(View):
    @aiohttp_jinja2.template('login.jinja2')
    async def get(self):
        return {'name': 'RaspManager'}
