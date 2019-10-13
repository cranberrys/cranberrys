from aiohttp import web

from board.handle import *


async def handler(request):
    location = request.app.router['index'].url_for()
    raise web.HTTPFound(location=location)


def router_set(app):
    app.router.add_static('/static', './board/static')

    app.router.add_get('/', handler)

    app.router.add_view('/login', LoginView, name='login')
    app.router.add_view('/index', IndexView, name='index')
    app.router.add_view('/error', ErrorView, name='error')

    app.router.add_view('/welcome', WelcomeView, name='welcome')
