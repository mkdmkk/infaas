from pymongo.mongo_client import MongoClient
from INFaaS import settings

__author__ = 'mkk'


if __name__ == "__main__":
    db = MongoClient()[settings.DB_NAME]

    # Drop collections
    db.users.drop()
    db.domains.drop()
    db.solutions.drop()
    db.contexts.drop()
    db.sources.drop()

    # Create collections
    db.create_collection("users")
    db.create_collection("domains")
    db.create_collection("solutions")

    # Create indexes
    db.users.create_index("email", unique=True)
    db.users.create_index("apikey", unique=True)
    db.domains.create_index("name", unique=True)
    db.solutions.create_index("name", unique=True)
    db.solutions.create_index("owner", unique=False)
