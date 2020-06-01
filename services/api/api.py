import logging

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from exception import exception_handler
from time_logger import time_logger

config = {'host': 'mongo', 'port': 27017, 'name': 'stock-exchanges'}

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s %(message)s')

mongo_client = AsyncIOMotorClient(host=config['host'], port=config['port'])
database = mongo_client[config['name']]

routes = web.RouteTableDef()


@routes.get('/api/v1/markets')
@time_logger
@exception_handler
async def handle_markets(request):
    collections = await database.list_collection_names()
    data = {
        collection: await database[collection].distinct('symbol')
        for collection in collections
    }
    logging.info(msg=f"Returned count: {len(data)}")
    return web.json_response(data, status=200)


@routes.get('/api/v1/trades')
@time_logger
@exception_handler
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


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=5005)
