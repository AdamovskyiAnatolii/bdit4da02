from motor.motor_asyncio import AsyncIOMotorClient


class DatabaseClient(object):
    """
        In case if we need to use the same database connection all the time.
    """
    __instance = {}

    def __init__(self, host: str, port: int):
        self._client: AsyncIOMotorClient = AsyncIOMotorClient(host=host, port=port)

    @staticmethod
    def get_instance(host: str, port: int) -> AsyncIOMotorClient:
        """
        Get database client instance for given connection host and port.

        :param host: host to connect to, e.g. 127.0.0.1
        :param port: port to connect to, e.g. 27017
        :return: long-live database client instance
        """
        if (host, port) not in DatabaseClient.__instance:
            DatabaseClient.__instance[(host, port)] = AsyncIOMotorClient(host=host, port=port)
        return DatabaseClient.__instance[(host, port)]
