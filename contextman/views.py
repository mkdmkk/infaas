'''
Context Management Service

Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
import json
from bson import json_util
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse

from contextman import ContextManager


@csrf_exempt
def process(request):

    cm = ContextManager()

    if request.method == 'GET':
        print("[contextman.view] Retrieving... %s" % request.GET)

        # Validation is needed.

        res_contexts = cm.retrieve(query=json.loads(request.GET["query"]), limit=int(request.GET["limit"]))
        return HttpResponse(json_util.dumps(res_contexts).encode("utf-8"), content_type="application/json")

    elif request.method == 'POST':
        print("[contextman.view] Inserting...")

        # Validation is needed.

        cm.insert(json.loads(request.body))
        return HttpResponse()

    elif request.method == 'DELETE':
        print("[contextman.view] Deleting...")

        # Validation is needed.

        cm.remove(json.loads(request.body))
        return HttpResponse()

    return HttpResponse()
