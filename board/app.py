import logging
import sys

from aiohttp import web

from setter.ac_api_setter import ac_api_set
from setter.module_setter import module_set
from setter.resource_setter import resource_set
from setter.router_setter import router_set

sys.path.append(".")

app = web.Application()

resource_set(app)
router_set(app)
ac_api_set(app)
module_set(app)

if __name__ == '__main__':
    logging.basicConfig(
        format='%(levelname)s: %(asctime)s [%(pathname)s:%(lineno)d] %(message)s',
        level=logging.NOTSET
    )
    web.run_app(app)
