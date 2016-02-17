from pymongo.mongo_client import MongoClient
from INFaaS import settings

__author__ = 'mkk'

class MongoDBManager():
    def __init__(self):
        self.db = MongoClient()[settings.DB_NAME]

    def drop_collections(self):
        self.db.users.drop()
        self.db.domains.drop()
        self.db.solutions.drop()
        self.db.contexts.drop()
        self.db.sources.drop()

    def init_collections(self):
        self.db.create_collection("users")
        self.db.create_collection("domains")
        self.db.create_collection("solutions")
        self.db.create_collection("contexts")
        self.db.create_collection("sources")

        self.db.users.create_index("email", unique=True)
        # self.db.domains.create_index("id", unique=True)
        # self.db.solutions.create_index("id", unique=True)
        # self.db.contexts.create_index("id", unique=True)
        # self.db.sources.create_index("id", unique=True)


if __name__ == "__main__":
    dbman = MongoDBManager()
    dbman.drop_collections()
    dbman.init_collections()
