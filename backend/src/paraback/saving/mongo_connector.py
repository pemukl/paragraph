import os

from pymongo import MongoClient


class MongoConnector:
    def __init__(self):

        connection_string = os.getenv('MONGO_LAWDB')
        if connection_string is None:
            connection_string = "mongodb://root:publicpw@localhost:27017"
        self.connection_string = connection_string

        lawdb = os.getenv('MONGO_LAWDB')
        if lawdb is None:
            lawdb = "laws"
        self.lawdb = lawdb


    def read(self, name):
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        res = collection.find_one({"abbreviation": name})
        client.close()
        return res

    def write(self, law):
        name = law.abbreviation
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        data = law.model_dump(exclude_none=True)
        data["_id"] = name
        collection.replace_one({"abbreviation": name}, data, upsert=True)
        client.close()
