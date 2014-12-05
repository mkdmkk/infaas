'''
Context Management Service

Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
import json
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy
from pymongo import MongoClient

import pymongo

from sklearn.naive_bayes import GaussianNB
from sklearn.tree.tree import DecisionTreeClassifier


@csrf_exempt
def infer(request):
    # Prepare db
    client = MongoClient()
    db = client.sis

    # Load application
    application = json.loads(request.body)

    # Load solution
    print("Loading solution... (%s)" % application["solution"])
    solution = db.solutions.find({"id": application["solution"]})[0]
    domain = db.domains.find({"id": solution["domain"]})[0]

    # Check algorithm
    if solution["alg"] == "c4.5":
        model = DecisionTreeClassifier()
    elif solution["alg"] == "gnb":
        model = GaussianNB()
    else:
        pass

    # Check solution
    print("Checking solution...")
    sit_list = []
    sit_base_list = []
    for sit, sit_base in solution["baseset"].iteritems():
        print(sit)
        print(sit_base)
        sit_list += [sit] * len(sit_base)
        sit_base_list += sit_base

    # Train model
    X = numpy.array(sit_base_list)
    y = numpy.array(sit_list)
    model.fit(X, y)

    # Infer situation
    results = model.predict(numpy.array(application["observation"]))

    print(results)

    return HttpResponse(results, content_type="application/json")


def convert_to_sequential_array(contexts_res):
    contexts_sequential_array = []
    # if contexts_res.count() > 0:
    # first_time = contexts_res[0]["time"]

    # dt_util = DateTimeUtil()
    for context_res in contexts_res:
        # dt_diff = dt_util.get_difference_as_seconds(first_time, context_res["time"]);
        # contexts_sequential_array.append([
        #     dt_diff,
        #     context_res["data"]["x"],
        #     context_res["data"]["y"],
        #     context_res["data"]["z"]])
        # contexts_sequential_array.append(dt_diff)
        contexts_sequential_array.append(float(context_res["data"]["x"]))
        contexts_sequential_array.append(float(context_res["data"]["y"]))
        contexts_sequential_array.append(float(context_res["data"]["z"]))

    return contexts_sequential_array
