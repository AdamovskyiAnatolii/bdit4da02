import ccxt.async_support as ccxt
from pymongo.errors import BulkWriteError, DuplicateKeyError

from .database import DatabaseClient
import config


class ExchangeReader(object):
    api = {}

    def __init__(self, exchange: str):
        self.exchange = exchange

        if exchange not in ExchangeReader.api:
            ExchangeReader.api[exchange] = eval(f'ccxt.{exchange}()')

        self.database = config.database['name']

    async def handle(self, symbol: str, limit: int):
        data = await self.api_call(symbol=symbol, limit=limit)
        stats = await self.write_to_database(data)

        return stats

    async def api_call(self, symbol: str, limit: int = 200):
        items = await ExchangeReader.api[self.exchange].fetch_trades(symbol=symbol, limit=limit)
        keys = ['id', 'timestamp', 'price', 'amount', 'symbol', 'side']

        return [{key: item[key] for key in keys} for item in items]

    async def write_to_database(self, data: list):
        total_inserted, total_amount = 0, len(data)

        port, host = config.database['port'], config.database['host']
        client = DatabaseClient.get_instance(host=host, port=port)

        collection = client[self.database][self.exchange]

        try:
            await collection.insert_many(data)
            total_inserted += len(data)
        except BulkWriteError:
            for item in data:
                try:
                    await collection.insert_one(item)
                    total_inserted += 1
                except DuplicateKeyError:
                    continue

        return total_inserted, total_amount
