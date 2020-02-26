from pymongo import MongoClient
import os


class MongoDBInstance:
    def __init__(self):
        self._client = MongoClient(os.getenv('MONGODB'))
        self._db = self._client[os.getenv('DATABASE')]
        self._coll = self._db[os.getenv('COLLECTION')]

    def insert_one(self, document):
        return self._coll.insert_one(document)

    def find_all(self, *args):
        return self._coll.find(*args)

    def count_documents(self, _filter):
        return self._coll.count_documents(_filter)