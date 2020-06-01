import logging
import time

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from exception import error_info

config = {'host': 'mongo', 'port': 27017, 'name': 'stock-exchanges'}

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s')

mongo_client = AsyncIOMotorClient(host=config['host'], port=config['port'])
database = mongo_client[config['name']]

routes = web.RouteTableDef()


@routes.get('/api/v1/markets')
async def handle_markets(request):
    collections = await database.list_collection_names()
    data = {
        collection: await database[collection].distinct('symbol')
        for collection in collections
    }
    logging.info(msg=f"Returned count: {len(data)}")
    return web.json_response(data, status=200)


@routes.get('/api/v1/trades')
async def trades_handle(request):
    """

    :param request:
        exchange
        symbol
        since
        limit
    :return:
    """
    params = request.rel_url.query

    exchange = params['exchange']
    query = {}

    if 'symbol' in params:
        query.update({'symbol': params['symbol'].upper().replace('_', '/')})

    if 'till' in params:
        query.update({'timestamp': {'$lte': int(params['till'])}})

    limit = min(int(params['limit']), 10000) if 'limit' in params else 100

    cursor = database[exchange]\
        .find(query, {'_id': 0})\
        .sort("timestamp", -1)\
        .limit(limit)

    data = [item async for item in cursor]
    logging.info(msg=f"Returned count: {len(data)}")

    return web.json_response(data, status=200)


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


app = web.Application(middlewares=[time_middleware, error_middleware])
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5005)
