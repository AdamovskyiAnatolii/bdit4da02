import time
import asyncio
import logging
from motor.motor_asyncio import AsyncIOMotorClient

from models.reader import ExchangeReader
import config



async def init_database():
    client = AsyncIOMotorClient(host=config.database['host'], port=config.database['port'])
    database_names = await client.list_database_names()
    database_name = config.database['name']

    if database_name not in database_names:
        logging.info(f'Start {database_name} initializing.')

        db = client[database_name]
        for collection_name in config.exchanges.keys():
            await db.create_collection(collection_name)
            await db[collection_name].create_index([('id', 1)], unique=True, background=False)
            await db[collection_name].create_index([('symbol', 1), ('time', 1)], background=False)

            logging.info(f'Initialized {database_name}.{collection_name}.')


async def run():
    readers = {name: ExchangeReader(name) for name in config.exchanges}

    while True:
        start_iter = time.time()

        for exchange, symbols in config.exchanges.items():
            for symbol in symbols:
                try:
                    inserted, total_requested = await readers[exchange].handle(symbol=symbol, limit=200)

                    logging.info(msg=str({'exchange': exchange,
                                          'symbol': symbol,
                                          'inserted': inserted,
                                          'total_requested': total_requested}))
                except Exception as e:
                    logging.info(msg=str({'exchange': exchange,
                                          'symbol': symbol,
                                          'error': str(e)[:200]}))

        end_iter = time.time()
        duration = end_iter - start_iter

        await asyncio.sleep(max(config.delay - duration, 0))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')

    asyncio.get_event_loop().run_until_complete(init_database())
    asyncio.get_event_loop().run_until_complete(run())
