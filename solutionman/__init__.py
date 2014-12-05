import simplejson
from comm import Communicator
from INFaaS import settings


def post_solution1():
    cq_walking = {}
    cq_walking["source"] = 1
    cq_walking["type"] = "acceleration"
    cq_walking["time"] = {}
    cq_walking["time"]["$gte"] = "2014-06-29T19:53:16"
    cq_walking["time"]["$lte"] = "2014-06-29T19:54:05"

    cq_jogging = {}
    cq_jogging["source"] = 1
    cq_jogging["type"] = "acceleration"
    cq_jogging["time"] = {}
    cq_jogging["time"]["$gte"] = "2014-06-29T20:10:26"
    cq_jogging["time"]["$lte"] = "2014-06-29T20:11:15"

    cq_running = {}
    cq_running["source"] = 1
    cq_running["type"] = "acceleration"
    cq_running["time"] = {}
    cq_running["time"]["$gte"] = "2014-06-29T20:13:29"
    cq_running["time"]["$lte"] = "2014-06-29T20:14:18"

    spec = {}
    spec["walking"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_walking)], "config": {}}
    spec["jogging"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_jogging)], "config": {}}
    spec["running"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_running)], "config": {}}

    solution = {}
    solution["id"] = 1
    solution["domain"] = "net.infidea.infaas.domain.humanactivityrecognition"
    solution["spec"] = spec
    solution["visibility"] = "public"

    comm = Communicator(settings.SERVER_HOST, settings.SERVER_PORT, "/api/solution")
    comm.post(solution)


def post_solution2():
    cq_walking = {}
    cq_walking["source"] = 2
    cq_walking["type"] = "acceleration"
    cq_walking["time"] = {}
    cq_walking["time"]["$gte"] = "49394992294000"
    cq_walking["time"]["$lte"] = "49400192306000"

    cq_jogging = {}
    cq_jogging["source"] = 2
    cq_jogging["type"] = "acceleration"
    cq_jogging["time"] = {}
    cq_jogging["time"]["$gte"] = "55161522233000"
    cq_jogging["time"]["$lte"] = "55165862260000"

    cq_standing = {}
    cq_standing["source"] = 2
    cq_standing["type"] = "acceleration"
    cq_standing["time"] = {}
    cq_standing["time"]["$gte"] = "3147192272000"
    cq_standing["time"]["$lte"] = "3149642253000"

    cq_sitting = {}
    cq_sitting["source"] = 2
    cq_sitting["type"] = "acceleration"
    cq_sitting["time"] = {}
    cq_sitting["time"]["$gte"] = "3041172314000"
    cq_sitting["time"]["$lte"] = "3043662242000"

    spec = {}
    spec["walking"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_walking)], "config": {}}
    spec["jogging"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_jogging)], "config": {}}
    spec["standing"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_standing)], "config": {}}
    spec["sitting"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_sitting)], "config": {}}

    solution = {}
    solution["id"] = 2
    solution["domain"] = "net.infidea.infaas.domain.humanactivityrecognition"
    solution["spec"] = spec
    solution["visibility"] = "public"

    comm = Communicator(settings.SERVER_HOST, settings.SERVER_PORT, "/api/solution")
    comm.post(solution)


def post_solution3():
    cq_walking = {}
    cq_walking["source"] = 2
    cq_walking["type"] = "acceleration"
    cq_walking["time"] = {}
    cq_walking["time"]["$gte"] = "49394992294000"
    cq_walking["time"]["$lte"] = "49400192306000"

    cq_jogging = {}
    cq_jogging["source"] = 2
    cq_jogging["type"] = "acceleration"
    cq_jogging["time"] = {}
    cq_jogging["time"]["$gte"] = "55161522233000"
    cq_jogging["time"]["$lte"] = "55165862260000"

    cq_standing = {}
    cq_standing["source"] = 2
    cq_standing["type"] = "acceleration"
    cq_standing["time"] = {}
    cq_standing["time"]["$gte"] = "3147192272000"
    cq_standing["time"]["$lte"] = "3149642253000"

    cq_sitting = {}
    cq_sitting["source"] = 2
    cq_sitting["type"] = "acceleration"
    cq_sitting["time"] = {}
    cq_sitting["time"]["$gte"] = "3041172314000"
    cq_sitting["time"]["$lte"] = "3043662242000"

    spec = {}
    spec["walking"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_walking)], "config": {}}
    spec["jogging"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_jogging)], "config": {}}
    spec["standing"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_standing)], "config": {}}
    spec["sitting"] = {"algo": "c4.5", "training": [simplejson.dumps(cq_sitting)], "config": {}}

    solution = {}
    solution["id"] = 3
    solution["domain"] = "net.infidea.infaas.domain.humanactivityrecognition"
    solution["spec"] = spec
    solution["visibility"] = "public"

    comm = Communicator(settings.SERVER_HOST, settings.SERVER_PORT, "/api/solution")
    comm.post(solution)


if __name__ == "__main__":
    post_solution1()
    post_solution2()
    post_solution3()
