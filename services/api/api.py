import logging
from aiohttp import web

from middlewares import error_middleware, time_middleware
from routes import routes


logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s')

app = web.Application(middlewares=[time_middleware, error_middleware])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5005)
