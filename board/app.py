from aiohttp import web

from module_setter import module_set
from resource_setter import resource_set
from router_setter import router_set
from scheduler_setter import scheduler_set

app = web.Application()

resource_set(app)
router_set(app)
scheduler_set(app)

module_set(app)

if __name__ == '__main__':
    web.run_app(app)
