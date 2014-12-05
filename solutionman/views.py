'''
Context Management Service

Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
from bson.json_util import dumps
from django.shortcuts import render_to_response
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from pymongo.mongo_client import MongoClient
import simplejson
from INFaaS import settings


BASE_PATH = 'solution/'
LIMIT = 5


def render(request, page):
    client = MongoClient()
    db = client[settings.DB_NAME]
    solutions = db.solutions

    context = Context()
    context['page'] = 'solution'
    if page == 'index':
        template = "index.html"
        res_solutions = solutions.find()
        res_solutions.limit(int(request.GET["limit"])) if request.GET.has_key("limit") else None
        context['solutions'] = res_solutions

    return render_to_response(BASE_PATH+template, context)


@csrf_exempt
def process(request):
    client = MongoClient()
    db = client[settings.DB_NAME]
    solutions = db.solutions

    if request.method == 'GET':
        solutionRetrieved = solutions.find({"id":request.GET["id"]})
        return HttpResponse(dumps(solutionRetrieved), content_type="application/json")

    elif request.method == 'POST':

        # Validation is needed.
        print("Inserting solution...")

        solutions.insert(simplejson.loads(request.body))
        return HttpResponse("Successful.", content_type="application/json")

    elif request.method == 'DELETE':
        pass

    return HttpResponse()
