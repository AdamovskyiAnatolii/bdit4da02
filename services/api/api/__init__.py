from .routes import routes
from .middlewares import error_middleware, time_middleware


def setup_routes(app):
    app.add_routes(routes)


def setup_middlewares(app):
    app.middlewares.append(time_middleware)
    app.middlewares.append(error_middleware)