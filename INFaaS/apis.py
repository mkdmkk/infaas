import json
import logging

from bson import ObjectId
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo.errors import DuplicateKeyError

from INFaaS import constants
from model.domain import DomainManager

logger = logging.getLogger(__name__)


@csrf_exempt
def handle_domains_mgt(request):
    try:
        m = DomainManager()
        if request.method == 'POST':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NODATA)
            data = json.loads(request.body.decode('utf-8'))
            if m.add_domain(data):
                return JsonResponse(constants.CODE_SUCCESS)
        elif request.method == 'GET':
            pass
        elif request.method == 'UPDATE':
            pass
        elif request.method == 'DELETE':
            if len(request.body) == 0:
                raise Exception(constants.MSG_NODATA)
            data = json.loads(request.body.decode('utf-8'))
            if '_id' in data:
                data['_id'] = ObjectId(data['_id'])
            if m.delete_domain(data):
                return JsonResponse(constants.CODE_SUCCESS)
    except DuplicateKeyError as e:
        msg = str(e)
    except Exception as e:
        msg = str(e)
    else:
        msg = "/api/domains"
    return JsonResponse({**constants.CODE_FAILURE, 'msg': msg})


@csrf_exempt
def handle_solutions_mgt(request):
    pass


@csrf_exempt
def handle_users_mgt(request):
    pass


@csrf_exempt
def infer(request):
    pass


@csrf_exempt
def hello(request):
    pass
