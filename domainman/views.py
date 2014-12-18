'''
Context Management Service

Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
import bson
from bson.json_util import dumps
from django.core.serializers import json
from django.shortcuts import render_to_response
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from pymongo.mongo_client import MongoClient
import simplejson

BASE_PATH = 'domain/'
LIMIT = 10

def render(request, page):
    client = MongoClient()
    db = client.sis
    domains = db.domains

    context = Context()
    context['page'] = 'domain'

    if page == 'index':
        template = "index.html"
        res_domains = domains.find()
        res_domains.limit(int(request.GET["limit"]) if request.GET.has_key("limit") else LIMIT)
        context['domains'] = res_domains

    return render_to_response(BASE_PATH+template, context)


@csrf_exempt
def process(request):
    client = MongoClient()
    db = client.sis
    domains = db.domains

    if request.method == 'GET':
        id = request.GET["id"]
        domain = domains.find({"id": id})
        return HttpResponse(dumps(domain), content_type="application/json")

    elif request.method == 'POST':
        domains.insert(simplejson.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        domains.remove(simplejson.load(request.body))
        return HttpResponse()

    return HttpResponse()
