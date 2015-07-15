from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from pymongo import MongoClient

import json
import numpy

import infengine


__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

@csrf_exempt
def infer(request):
    """
    Handle inference request
    :param request: inference request sent from a client
    :return: inference result
    """
    # Prepare db
    client = MongoClient()
    db = client.sis

    # Load application
    application = json.loads(request.body)

    # Load solution
    print("Loading solution... (%s)" % application["solution"])
    solution = db.solutions.find({"id": application["solution"]})[0]
    domain = db.domains.find({"id": solution["domain"]})[0]

    # Prepare model
    model = infengine.prepare_model(solution, domain)
    print("The model is prepared: %s" % model)

    # Train model
    infengine.train_model(model, *infengine.load_basesets(solution))

    # Infer situation
    if solution["alg"] in infengine.ALGS_CLASSIFICATION:
        obs = numpy.array(application["observation"])
        result = model.predict(obs)
        confidence = model.predict_proba(obs)
        print("The situation is inferred: %s" % result)

        return HttpResponse(json.dumps({"result": str(result), "confidence": str(confidence)}).encode("utf-8"), content_type="application/json")
    elif solution["alg"] in infengine.ALGS_CLUSTERING:
        if "observation" in application:
            results = model.predict(numpy.array(application["observation"]))
            print("Result of inference: %s" % results.tolist()[0])
        print("Result of clustering: %s" % model.labels_.tolist())
        return HttpResponse(json.dumps({"baseset":model.labels_.tolist(),"observation":results.tolist()[0]}).encode("utf-8"), content_type="application/json")
    else:
        return HttpResponse("No result.", content_type="application/json")

