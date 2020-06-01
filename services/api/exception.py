import json
import sys
from functools import wraps
from typing import Callable, Dict

from aiohttp import web


def exception_handler(func: Callable) -> Callable:
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            err = error_info(e)
            return web.Response(text=json.dumps({"error": err}, indent=4),
                                status=400)

    return decorated_function


def error_info(e: Exception) -> Dict[str, str]:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    err = {
        'type': str(exc_type.__name__),
        'text': str(exc_obj),
    }
    return err
