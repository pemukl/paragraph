import os
import re

from pymongo import MongoClient

from paraback.models.law_model import Law
from dotenv import load_dotenv



class MongoConnector:
    def __init__(self, db=None, collection=None):
        load_dotenv(os.path.join(os.getcwd(), ".env"))

        self.connection_string = os.getenv('MONGO_URI')

        if not self.test_connection():
            self.connection_string = f"mongodb://{os.getenv('MONGO_ROOT_USERNAME')}:{os.getenv('MONGO_ROOT_PASSWORD')}@localhost:27017"

        db = db or os.getenv('MONGO_LAWDB') or "laws"

        collection = collection or "de"

        self.lawdb = db
        self.collection = collection


    def test_connection(self):
        try:
            client = MongoClient(self.connection_string)
            client.server_info()
            client.close()
            return True
        except Exception as e:
            print(e)
            return False

    def read(self, stemmedabbreviation: str):
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        res = collection.find_one({"stemmedabbreviation": stemmedabbreviation})
        client.close()
        if "_id" in res:
            del res["_id"]
        return Law.model_validate(res)

    def read_all(self):
        names = self._all_names()
        return (self.read(name) for name in names)

    def _all_names(self):
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db[self.collection]
        res = collection.find({})
        names = [x["stemmedabbreviation"] for x in res]
        client.close()
        return names


    def read_important(self):
        names = self._important_names()

        return (self.read(name) for name in names)

    def read_essential(self):
        names = ["eWpG", "AktG","BGB", "DepotG", "BMG"]

        return (self.read(name) for name in names)

    def count_important(self):
        names = self._important_names()
        return len(names)

    def count_all(self):
        names = self._all_names()
        return len(names)

    def _important_names(self):
        names = self._all_names()
        to_be_ignored = lambda x:(
                x.endswith("V")
                or x.endswith("AnO")
                or "Bek" in x
                or "Abk" in x
                or "Prot" in x
                or "Übk" in x
                or "Prot" in x
                or x.endswith("Ber")
                or re.search(r'\d+$', x)
                or re.search(r'\d\d\d\d', x)
        )
        return [x for x in names if not to_be_ignored(x)]



    def write(self, law: Law):
        law_id = law.stemmedabbreviation
        client = MongoClient(self.connection_string)
        db = client[self.lawdb]
        collection = db['de']
        data = law.model_dump(exclude_none=True)
        collection.replace_one({"stemmedabbreviation": law_id}, data, upsert=True)
        client.close()

    def clear_names(self):
        client = MongoClient(self.connection_string)
        db = client["names"]
        collection = db['de_names']
        collection.delete_many({})
        client.close()

    def overwrite_names(self, names_dict: dict):
        #get the current names fom the db
        client = MongoClient(self.connection_string)
        db = client["names"]
        collection = db['de_names']
        collection.replace_one({}, names_dict, upsert=True)
        client.close()

    def write_name(self, names_dict: dict):
        names = self.read_all_names()
        if names is None:
            names = {}
        else:
            names.update(names_dict)
        self.overwrite_names(names)


    def read_all_names(self):
        client = MongoClient(self.connection_string)
        db = client["names"]
        collection = db['de_names']
        names = collection.find_one()
        client.close()
        return names