'''
Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import Context
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
import simplejson
from INFaaS import settings

import sourceman.views as sourceman


@csrf_exempt
def process(request):
    client = MongoClient()
    db = client[settings.DB_NAME]
    users = db.users

    if request.method == 'GET':

        print(request.GET)

        # Validation is needed.

        res_contexts = users.find(simplejson.loads(request.GET["query"]))
        if request.GET.has_key("limit"):
            res_contexts.limit(int(request.GET["limit"]))

        return HttpResponse(simplejson.dumps(res_contexts), content_type="application/json")

    elif request.method == 'POST':

        # Validation is needed.

        print("Inserting user...")

        users.insert(simplejson.loads(request.body))
        return HttpResponse()

    elif request.method == 'UPDATE':

        # Validation is needed.

        print("Updating user...")

        users.update(simplejson.loads(request.body))
        return HttpResponse()


    elif request.method == 'DELETE':

        # Validation is needed.

        users.remove(simplejson.loads(request.body))
        return HttpResponse()

    return HttpResponse()
