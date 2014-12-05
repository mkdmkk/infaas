from comm import Communicator
from INFaaS import settings


def post_domain1():
    domain = {}
    domain["id"] = "net.infidea.infaas.domain.handgesturerecognition"
    domain["name"] = "Hand Gesture Recognition"
    domain["version"] = "0.1"
    domain["description"] = "To recognize hand gesture from acceleration contexts"
    domain["situations"] = ["shaking"]
    comm = Communicator(settings.SERVER_HOST, settings.SERVER_PORT, "/api/domain")
    comm.post(domain)


def post_domain2():
    domain = {}
    domain["id"] = "net.infidea.infaas.domain.humanactivityrecognition"
    domain["name"] = "Human Activity Recognition"
    domain["version"] = "0.1"
    domain["description"] = "To recognize human movement from acceleration contexts"
    domain["situations"] = ["walking", "jogging", "standing", "sitting"]
    comm = Communicator(settings.SERVER_HOST, settings.SERVER_PORT, "/api/domain")
    comm.post(domain)
