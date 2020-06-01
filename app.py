import time
import asyncio
import numpy as np

from models.reader import ExchangeReader
import config


async def run():
    readers = {name: ExchangeReader(name) for name in config.exchanges}

    while True:
        start_iter = time.time()

        for exchange, symbols in config.exchanges.items():
            for symbol in symbols:
                try:
                    stats = await readers[exchange].handle(symbol=symbol, limit=200)

                    print(f"[{np.datetime64('now', 's')}] ({exchange:>12}, {symbol:<12}) - Inserted: {stats}")
                except Exception as e:
                    print(f"[{np.datetime64('now', 's')}] ({exchange:>12}, {symbol:<12}) - Error: {e}")

        end_iter = time.time()
        duration = end_iter - start_iter

        await asyncio.sleep(max(config.delay - duration, 0))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(run())
