import aiohttp_jinja2
import jinja2
from aiohttp import web

from board.view.error import ErrorView
from board.view.index import IndexView
from board.view.login import LoginView
from board.view.module.welcome import WelcomeView
from view.module.everphoto_checkin import EverPhotoCheckInView


async def handler(request):
    location = request.app.router['index'].url_for()
    raise web.HTTPFound(location=location)


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./board/templates'))
app.router.add_static('/static', './board/static')

app.router.add_get('/', handler)
app.router.add_view('/login', LoginView, name='login')
app.router.add_view('/index', IndexView, name='index')
app.router.add_view('/error', ErrorView, name='error')

app.router.add_view('/welcome', WelcomeView, name='welcome')

app.router.add_view('/auto_check_in', EverPhotoCheckInView, name='auto_check_in')

app.router.add_view('/welcome1', WelcomeView, name='welcome1')
app.router.add_view('/welcome2', WelcomeView, name='welcome2')


if __name__ == '__main__':
    web.run_app(app)
