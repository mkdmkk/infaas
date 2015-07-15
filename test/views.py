'''
Test API
Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
import json
from bson import json_util
from django.http.response import HttpResponse

def hello(request):

    if request.method == 'GET':
        print("[Test] Say Hello.")
        res = {}
        res["result"] = "Hello"
        return HttpResponse(json.dumps(res), content_type="application/json")

    elif request.method == 'POST':
        return HttpResponse()

    elif request.method == 'PUT':
        return HttpResponse()

    elif request.method == 'DELETE':
        return HttpResponse()

    return HttpResponse()
