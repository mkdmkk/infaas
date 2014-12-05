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

    #
    # training_sets = []
    # labels = []
    # idx = 1
    # for situation_spec in spec:
    #     for cq_training in situation_spec["training"]:
    #         print("Query: %s" % cq_training)
    #         # Temp
    #         contexts_res = db.contexts.find(json.loads(cq_training)).limit(50).sort('time', pymongo.ASCENDING)
    #         contexts_sequential_array = convert_to_sequential_array(contexts_res)
    #         training_sets.append(contexts_sequential_array)
    #         labels.append(idx)
    #
    #     idx += 1
    #
    # knowledge_model = GaussianNB()
    # print(numpy.array(training_sets))
    # print(numpy.array(labels))
    # knowledge_model.fit(numpy.array(training_sets), numpy.array(labels))
    # print(knowledge_model.predict_log_proba(numpy.array(training_sets[0])))
    # print(knowledge_model.predict_log_proba(numpy.array(training_sets[1])))
    # print(knowledge_model.predict_log_proba(numpy.array(training_sets[2])))
    # print(knowledge_model.predict_log_proba(numpy.array(training_sets[3])))
    # observation_contexts = db.contexts.find(application["observation"]).limit(50).sort('time', pymongo.ASCENDING)
    # contexts_sequential_array = convert_to_sequential_array(observation_contexts)
    # print(contexts_sequential_array)
    # prob_results = knowledge_model.predict_log_proba(numpy.array(contexts_sequential_array))
    # print(prob_results)

    # return HttpResponse(json.loads(prob_results), content_type="application/json")

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
