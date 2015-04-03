from pymongo import MongoClient, ASCENDING, DESCENDING
import json
from bson import json_util

from INFaaS import settings

__author__ = 'mkk'

DEFAULT_LIMIT = 100

class ContextManager:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[settings.DB_NAME]
        self.contexts = self.db.contexts

    def retrieve(self, query=None, limit=None):
        """
        To retrieve contexts
        :param query: JSON Object; Mongo DB query
        :param limit: int;
        :return:
        """
        if query:
            res_contexts = self.contexts.find(query)
            if limit:
                res_contexts = res_contexts.limit(limit)
        else:
            res_contexts = self.contexts.find().sort("time", DESCENDING).limit(DEFAULT_LIMIT)
        return res_contexts

    def insert(self, data):
        """
        To insert contexts
        :param data: JSON Object; context to insert
        :return:
        """
        self.contexts.insert(data)

    def remove(self, data):
        self.contexts.remove(json.loads(data))