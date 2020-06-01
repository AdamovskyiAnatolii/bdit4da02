import logging
from aiohttp import web

from api import routes, middlewares

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s')

app = web.Application(middlewares=middlewares)
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5005)
