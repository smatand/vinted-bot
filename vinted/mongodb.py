import motor.motor_asyncio as motor
from settings import MONGODB_CONNSTRING

COLL_NAME = "vinted"
MONGODB_NAME = "vinted"


class MongoDB:
    def __init__(self, conn_string=MONGODB_CONNSTRING, db_name=MONGODB_NAME,
                 collection_name=COLL_NAME):
        self._conn = motor.AsyncIOMotorClient(conn_string)
        self._db = self._conn[db_name]
        self._collection = self._db[collection_name]

    async def insert(self, item):
        """Inserts an item to the database

        Keyword arguments:
        item -- the item to insert
        """
        await self._collection.insert_one(item)

    async def find(self, query):
        """Finds items in the database

        Keyword arguments:
        query -- the query to search for
        """
        return self._collection.find(query)
    
    async def delete(self, query):
        """Deletes items from the database

        Keyword arguments:
        query -- the query to search for
        """
        return self._collection.delete_many(query)