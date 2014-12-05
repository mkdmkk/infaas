'''
Context Management Service

Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
import bson
from bson.json_util import dumps
from django.core.serializers import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from pymongo.mongo_client import MongoClient
import simplejson
from INFaaS import settings


@csrf_exempt
def process(request):
    client = MongoClient()
    db = client[settings.DB_NAME]
    contexts = db.contexts

    if request.method == 'GET':

        print(request.GET)

        # Validation is needed.

        res_contexts = None
        if request.GET.has_key("limit"):
            res_contexts = contexts.find(simplejson.loads(request.GET["query"])).limit(int(request.GET["limit"]))
        else:
            res_contexts = contexts.find(simplejson.loads(request.GET["query"]))

        return HttpResponse(dumps(res_contexts), content_type="application/json")

    elif request.method == 'POST':

        # Validation is needed.

        print("Inserting context...")

        contexts.insert(simplejson.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':

        # Validation is needed.

        contexts.remove(simplejson.loads(request.body))
        return HttpResponse()

    return HttpResponse()
