from bson.json_util import dumps
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from pymongo.mongo_client import MongoClient
import simplejson

QUERY_LIMIT = 100

@csrf_exempt
def process(request):
    client = MongoClient()
    db = client.sis

    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

    return HttpResponse()


def crud(action):
    client = MongoClient()
    db = client.sis
    sources = db.sources

    if action == 'c':
        pass
    elif action == 'r':
        res = sources.find().limit(QUERY_LIMIT)
        return res
    elif action == 'u':
        pass
    elif action == 'd':
        pass
