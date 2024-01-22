import os

from pymongo import MongoClient

from paraback.models.law_model import Law


class MongoConnector:
    def __init__(self, db=None, collection=None):

        connection_string = os.getenv('MONGO_URI')
        self.connection_string = connection_string

        db = db or os.getenv('MONGO_LAWDB') or "laws"

        collection = collection or "de"

        self.lawdb = db
        self.collection = collection


    def read(self, stemmedabbreviation: str):
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        res = collection.find_one({"abbreviation": stemmedabbreviation})
        client.close()
        return Law.model_validate(res)

    def write(self, law: Law):
        law_id = law.stemmedabbreviation
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        data = law.model_dump(exclude_none=True)
        collection.replace_one({"stemmedabbreviation": law_id}, data, upsert=True)
        client.close()

    def write_name(self, law: Law):
        #get the current names fom the db
        client = MongoClient(self.connection_string)
        db = client["names"]
        collection = db['de_names']
        res = collection.find_one({})
        if res is None:
            res = {}
        res[law.abbreviation] = law.stemmedabbreviation
        if law.longname is not None:
            res[law.longname] = law.stemmedabbreviation
        if law.title is not None:
            res[law.title] = law.stemmedabbreviation
        collection.replace_one({}, res, upsert=True)
        client.close()


    def read_all_names(self):
        client = MongoClient(self.connection_string)
        db = client["names"]
        collection = db['de_names']
        names = collection.find_one()
        client.close()
        return names