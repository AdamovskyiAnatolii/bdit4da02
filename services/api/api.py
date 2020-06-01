import json
import time
import logging

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient


config = {'host': 'mongo', 'port': 27017, 'name': 'stock-exchanges'}


logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')

mongo_client = AsyncIOMotorClient(host=config['host'], port=config['port'])
database = mongo_client[config['name']]

routes = web.RouteTableDef()


@routes.get('/api/v1/markets')
async def handle_markets(request):
    try:
        start_time = time.time()

        collections = await database.list_collection_names()

        data = {}
        for collection in collections:
            data[collection] = await database[collection].distinct('symbol')

        end_time = time.time()

        logging.info(msg=f"Total time: {round(end_time - start_time, 4)}, Returned count: {len(data)}")

        return web.Response(text=json.dumps(data, indent=4), status=200)

    except Exception as e:
        return web.Response(text=json.dumps({"error": str(e)}, indent=4), status=400)


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

    try:
        start_time = time.time()

        params = request.rel_url.query

        exchange = params['exchange']
        query = {}

        if 'symbol' in params:
            query.update({'symbol': params['symbol'].upper().replace('_', '/')})

        if 'limit' in params:
            limit = min(int(params['limit']), 10000)
        else:
            limit = 100

        if 'till' in params:
            query.update({'timestamp': {'$lte': int(params['till'])}})

        cursor = database[exchange]\
            .find(query, {'_id': 0})\
            .sort("timestamp", -1)\
            .limit(limit)

        data = []
        async for item in cursor:
            data.append(item)

        end_time = time.time()

        logging.info(msg=f"Total time: {round(end_time - start_time, 4)}, Returned count: {len(data)}")

        return web.Response(text=json.dumps(data, indent=4), status=200)

    except Exception as e:
        return web.Response(text=json.dumps({"error": str(e)}, indent=4), status=400)


app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app, port=5005)
