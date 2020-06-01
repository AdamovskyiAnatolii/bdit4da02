import time
import asyncio
import logging

from models.reader import ExchangeReader
import config


async def run():
    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s %(message)s')

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
    asyncio.get_event_loop().run_until_complete(run())
