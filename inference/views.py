from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from sklearn.cluster.k_means_ import KMeans
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors.classification import KNeighborsClassifier
from sklearn.svm.classes import SVC
from sklearn.tree.tree import DecisionTreeClassifier
from hmmlearn.hmm import GaussianHMM

from pymongo import MongoClient

import json
import numpy


__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'


# Supported Classification Algorithms
ALGS_CLASSIFICATION = [
    "c4.5",     # Decision Tree (DT): C4.5
    "cart",     # Decision Tree (DT): CART
    "gnb",      # Gaussian Naive Bayes (GNB)
    "svm",      # Support Vector Machine (SVM)
    "knn",      # K-Nearest Neighbor (KNN)
    "adaboost", # AdaBoost
    "hmm"       # Hidden Markov Model (HMM)
]

# Supported Clustering Algorithms
ALGS_CLUSTERING = [
    "kmeans"    # K-Means Clustering
]

# Default configuration for each algorithm
DEFAULT_CONF = {
    "kmeans": {"num_clusters": 4},
    "hmm": {"num_states": 4, "algo":"viterbi"}
}

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
    model = _prepare_model(solution, domain)
    print("The model is prepared: %s" % model)

    # Train model
    _train_model(model, *_load_basesets(solution))

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


def _prepare_model(solution, domain):
    """
    Prepare model based on solution and domain
    :rtype : object
    :param solution: specification of algorithm and configuration
    :param domain: a set of situations (labels)
    :return: prepared model or None
    """
    # The following algorithm types are considered: classification, clustering
    if solution["alg"] == "c4.5":
        model = DecisionTreeClassifier(criterion="entropy")
    elif solution["alg"] == "cart":
        model = DecisionTreeClassifier(criterion="gini")
    elif solution["alg"] == "gnb":
        model = GaussianNB()
    elif solution["alg"] == "svm":
        model = SVC()
    elif solution["alg"] == "knn":
        model = KNeighborsClassifier(1)
    elif solution["alg"] == "adaboost":
        model = AdaBoostClassifier()
    elif solution["alg"] == "kmeans":
        # Configuration for KMeans:
        # num_clusters: the number of clusters

        # Check configuration
        if "conf" in solution and "num_clusters" in solution["conf"]:
            num_clusters = solution["conf"]["num_clusters"]
        else:
            num_clusters = len(domain["situations"])
        print("The decided number of clusters is %s." % num_clusters)
        model = KMeans(n_clusters=num_clusters)
    elif solution["alg"] == "hmm":
        # Configuration for HMM:
        # num_states: the number of hidden states

        model = {}
        for s in domain.situations:
            model[s] = GaussianHMM(int(solution["conf"]["num_states"]) if "conf" in solution and "num_states" in solution["conf"] else DEFAULT_CONF["hmm"]["num_states"], algorithm='viterbi', covariance_type='diag')

    return model


def _load_basesets(solution):
    """
    Load base set for supervised learning algorithms
    :param solution: solution containing base set
    :return: base set
    """
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
    if baseset_lbs:
        y = numpy.array(baseset_lbs)
        model.fit(X, y) # Supervised Learning



    # X = np.reshape(data, (len(data),1))
    # self.model = self.model.fit([X])
    #
    # self.hidden_states = self.model.predict(X)
    # print(self.hidden_states)

    #
    # # Train the HMMs by the solution
    # for s, seq in solution.baseset:
    #     model[s].fit(seq)
    #
    # # Classify the observations specified in the application
    # max_prob = None
    # result_sit = None
    # for s, model in models:
    #     prob = model.predict(application.observation)
    #     if not max_prob or max_prob <= prob:
    #         max_prob = prob
    #         result_sit = s
    #
    # return result_sit