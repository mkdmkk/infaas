import json
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import numpy
from pymongo import MongoClient
from sklearn.cluster.k_means_ import KMeans

from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.svm.classes import SVC
from sklearn.tree.tree import DecisionTreeClassifier

from hmmlearn.hmm import GaussianHMM


__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'


ALGS_CLASSIFICATION = ["c4.5", "gnb", "svm", "knn", "hmm"]
ALGS_CLUSTERING = ["kmeans"]


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

    # Check algorithm and prepare model
    # The following algorithm types are considered: classification, clustering
    # The following algorithms are supported:
    # Decision Tree (c.4.5), Gaussian Naive Bayes (gnb), Support Vector Machine (svm),
    # K-Nearest Neighbors (knn), K-Means Clustering (kmeans)
    if solution["alg"] == "c4.5":
        model = DecisionTreeClassifier()
    elif solution["alg"] == "gnb":
        model = GaussianNB()
    elif solution["alg"] == "svm":
        model = SVC()
    elif solution["alg"] == "knn":
        model = KNeighborsClassifier(1)
    elif solution["alg"] == "kmeans":
        # Check configuration
        if "conf" in application and "num_clusters" in application["conf"]:
            num_clusters = application["conf"]["num_clusters"]
        elif "conf" in solution and "num_clusters" in solution["conf"]:
            num_clusters = solution["conf"]["num_clusters"]
        else:
            num_clusters = len(domain["situations"])
        print("The decided number of clusters is %s." % num_clusters)
        model = KMeans(n_clusters=num_clusters)
    elif solution["alg"] == "hmm":
        return HttpResponse(json.dumps(_run_hmm(application, domain, solution)), content_type="application/json")
    else:
        return HttpResponse("The specified algorithm, %s, is not supported yet." % solution["alg"], content_type="application/json")

    print("The model is prepared: %s" % model)

    # Train model
    _train_model(model, *_load_solution(solution))

    # Infer situation
    if solution["alg"] in ALGS_CLASSIFICATION:
        results = model.predict(numpy.array(application["observation"]))
        print("The situation is inferred: %s" % results)
        return HttpResponse(results, content_type="application/json")
    elif solution["alg"] in ALGS_CLUSTERING:
        if "observation" in application:
            results = model.predict(numpy.array(application["observation"]))
            print("Result of inference: %s" % results.tolist()[0])
        print("Result of clustering: %s" % model.labels_.tolist())
        return HttpResponse(json.dumps({"baseset":model.labels_.tolist(),"observation":results.tolist()[0]}), content_type="application/json")
    else:
        return HttpResponse("No result.", content_type="application/json")


def _load_solution(solution):
    print("Loading solution...")
    if type(solution) is dict: # Supervised Learning
        baseset_lbs = []
        basesets = []
        for lb, baseset in solution["baseset"].iteritems():
            print("The situation loaded. %s: %s" % (lb, baseset))
            baseset_lbs += [lb] * len(baseset)
            basesets += baseset
        return basesets, baseset_lbs
    elif type(solution) is list: # Unsupervised Learning
        pass


def _train_model(model, basesets, baseset_lbs):
    """
    Train model
    :param model:
    :param basesets:
    :param baseset_lbs: {optional} label for each base set
    :return: trained model
    """
    print("Training model...")
    X = numpy.array(basesets)
    if baseset_lbs != None:
        y = numpy.array(baseset_lbs)
        model.fit(X, y) # Supervised Learning


def _run_hmm(application, domain, solution):
    """
    Run hmm
    :return:
    """
    # Prepare multiple HMMs
    models = {}
    for s in domain.situations:
        models[s] = GaussianHMM()

    # Train the HMMs by the solution
    for s, seq in solution.baseset:
        models[s].fit(seq)

    # Classify the observations specified in the application
    max_prob = None
    result_sit = None
    for s, model in models:
        prob = model.predict(application.observation)
        if not max_prob or max_prob <= prob:
            max_prob = prob
            result_sit = s

    return result_sit