import asyncio
import json

import aiohttp
import aiohttp_jinja2
from aiohttp.web_urldispatcher import View

from data_manager import data

BASE_URL = 'https://api.everphoto.cn'


async def check_mobile(mobile, country_code='+86'):
    async with aiohttp.request(
            f'GET',
            f'{BASE_URL}/auth/mobile/check',
            params={'mobile': mobile, 'country_code': country_code}
    ) as resp:
        content = await resp.json()
        pass
    pass


async def smscode(mobile):
    async with aiohttp.request(
            f'POST',
            f'{BASE_URL}/smscode',
            params=json.dumps({'mobile': mobile})
    ) as resp:
        content = await resp.json()
        pass
    pass


async def login(mobile, smscode):
    async with aiohttp.request(
            f'POST',
            f'{BASE_URL}/auth',
            data=json.dumps({'mobile': mobile, 'smscode': smscode})
    ) as resp:
        content = await resp.json()
        pass
    pass


async def checkin_post(token):
    async with aiohttp.request(
            f'POST',
            f'{BASE_URL}/users/self/checkin/v2',
            headers={'Authorization': f'Bearer {token}'}
    ) as resp:
        content = await resp.json()
        pass
    pass


async def checkin_query(token):
    async with aiohttp.request(
            f'GET',
            f'{BASE_URL}/users/self/checkin/v2',
            headers={'Authorization': f'Bearer {token}'}
    ) as resp:
        content = await resp.json()
        pass
    pass


class AutoCheckInView(View):
    @aiohttp_jinja2.template('module/auto_check_in.html')
    async def get(self):
        token = data.get('token', '')
        if token:
            return {'name': 'RaspManager'}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(checkin_query('123'))
