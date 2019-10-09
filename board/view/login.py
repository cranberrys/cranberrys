import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class LoginView(View):
    @aiohttp_jinja2.template('login.html')
    async def get(self):
        return {'name': 'RaspManager'}
