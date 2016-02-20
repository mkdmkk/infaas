import logging

from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


@csrf_exempt
def handle_domains_mgt(request):
    pass

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
