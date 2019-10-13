import aiohttp_jinja2
import jinja2
from aiohttp import web

from board.module_setter import module_set
from board.router_setter import router_set
from board.scheduler_setter import scheduler_set

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./board/template'))

router_set(app)
scheduler_set(app)

module_set(app)

if __name__ == '__main__':
    web.run_app(app)
