from pymongo import MongoClient

from INFaaS import settings


# Context types
WEIGHT = "weight"           # kg
HEIGHT = "height"           # meter
FAT = "fat"                 # kg
DIASTOLIC = "diastolic"     # mmHg
SYSTOLIC = "systolic"       # mmHg
PULSE = "pulse"             # bpm
SPO2 = "spo2"               # %


class ContextManager:
    """ Manages contexts.

    Context format: {timestamp, type, data}
        timestamp: int; datetime as unix epoch
        type: str; context type
        data:
    """
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client[settings.DB_NAME]
        self.contexts = self.db.contexts

    def retrieve(self, query=None, sort_key="time", sort_order="desc", limit=100):
        """
        To retrieve contexts
        :param query: JSON Object; Mongo DB query
        :param limit: int;
        :return:
        """

        # Validation
        if sort_order not in ["ask", "desc"]:
            raise "Wrong sorting order."

        if query:
            res_contexts = self.contexts.find(query)
            if limit:
                res_contexts = res_contexts.limit(limit)
        else:
            res_contexts = self.contexts.find().sort(sort_key, DESCENDING if sort_order == "desc" else ASCENDING).limit(100)
        return res_contexts

    def insert(self, data):
        """
        To insert contexts
        :param data: JSON Object; context to insert
        :return:
        """
        return self.contexts.insert_one(data)

    def remove(self, data):
        self.contexts.delete_one(json.loads(data))