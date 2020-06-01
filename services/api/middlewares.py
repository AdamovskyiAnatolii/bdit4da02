import logging
import time

from aiohttp import web

from exception import error_info


async def error_middleware(app, handler):
    async def middleware_handler(request):
        try:
            return await handler(request)
        except Exception as ex:
            err = error_info(ex)
            return web.json_response({"error": err}, status=500)

    return middleware_handler


async def time_middleware(app, handler):
    async def middleware_handler(request):
        start_time = time.time()
        res = await handler(request)
        end_time = time.time()
        logging.info(msg=f"Total time: {round(end_time - start_time, 4)}")
        return res

    return middleware_handler
