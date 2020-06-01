import json
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

import config


mongo_client = AsyncIOMotorClient(host=config.database['host'], port=config.database['port'])
database = mongo_client[config.database['name']]

routes = web.RouteTableDef()


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

        return web.Response(text=json.dumps(data, indent=4), status=200)

    except Exception as e:
        return web.Response(text=json.dumps({"error": str(e)}, indent=4), status=400)


app = web.Application()
app.add_routes(routes)


if __name__ == '__main__':
    web.run_app(app, port=5000)