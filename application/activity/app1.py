import httplib2
import json
from INFaaS import settings

"""
App for Human Activity Recognition
"""
def request():
    # Prepare connection to INFaaS
    conn = httplib2.HTTPConnection(settings.SERVER_HOST, settings.SERVER_PORT)

    # Prepare contexts for testing
    context_query = {}
    context_query["source"] = 2
    context_query["type"] = "acceleration"
    context_query["time"]["$gte"] = "49405512314000"
    context_query["time"]["$lte"] = "49475072342000"

    # Prepare application to request
    application = {}
    application["user"] = "mkdmkk@gmail.com"
    application["solution"] = "net.infidea.infaas.solution.humanactivityrecognition"
    application["observation"] = context_query

    # Request situation inference
    conn.request("POST", "/api/infer", json.dumps(application), headers={"Content-Type": "application/json"})

    # Get result of inference
    response = conn.getresponse()
    print(json.loads(response))