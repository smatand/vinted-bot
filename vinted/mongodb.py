from pymongo import MongoClient
from settings import MONGODB_CONNSTRING

COLL_NAME = "vinted"
MONGODB_NAME = "vinted"


class MongoDB:
    def __init__(self, conn_string=MONGODB_CONNSTRING, db_name=MONGODB_NAME,
                 collection_name=COLL_NAME):
        self._conn = MongoClient(conn_string)
        self._db = self._conn[db_name]
        self._collection = self._db[collection_name]

    def insert(self, data):
        return self._collection.insert_one(data)

    def delete(self, data):
        return self._collection.delete_one(data)

    def print_all(self):
        for doc in self._collection.find():
            print(doc)

    def drop_collection(self):
        self._collection.drop()
