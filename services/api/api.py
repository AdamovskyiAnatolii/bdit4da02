import logging
from aiohttp import web

from api import setup_routes, setup_middlewares

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s')

app = web.Application()
setup_routes(app)
setup_middlewares(app)

if __name__ == '__main__':
    web.run_app(app, port=5005)
