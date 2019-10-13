import aiohttp_jinja2
from aiohttp.web_urldispatcher import View


class ErrorView(View):
    @aiohttp_jinja2.template('error.jinja2')
    async def get(self):
        return {'name': 'RaspManager'}
