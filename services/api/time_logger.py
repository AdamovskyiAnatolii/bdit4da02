import logging
import time
from functools import wraps
from typing import Callable


def time_logger(func: Callable) -> Callable:
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        start_time = time.time()
        res = await func(*args, **kwargs)
        end_time = time.time()
        logging.info(msg=f"Total time: {round(end_time - start_time, 4)}")

        return res

    return decorated_function
