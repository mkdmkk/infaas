import httplib
import random
import datetime
import simplejson
import time
from INFaaS import settings

__author__ = 'mkk'

class ContextTransmitter(object):
    def __init__(self, host, port, url):
        self.url = url
        self.conn = httplib.HTTPConnection(host, port)

    def generate(self):
        pass

    def post(self, context):
        print(context)
        self.conn.request("POST", self.url, simplejson.dumps(context), headers={"Content-Type": "application/json"})
        response = self.conn.getresponse()
        print(response.status)

    def start(self):
        while True:
            self.post(self.generate())
            time.sleep(1)

class AccelerationContextTransmitter(ContextTransmitter):
    def __init__(self, host, port, url, minVal=-20, maxVal=20):
        super(AccelerationContextTransmitter, self).__init__(host, port, url)
        self.minVal = minVal
        self.maxVal = maxVal

    def generate(self):
        context = {}
        context["source"] = 1
        context["type"] = "acceleration"
        context["time"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        data = {}
        data["x"] = round(random.uniform(self.minVal, self.maxVal),6)
        data["y"] = round(random.uniform(self.minVal, self.maxVal),6)
        data["z"] = round(random.uniform(self.minVal, self.maxVal),6)
        context["data"] = data
        return context

if __name__ == "__main__":
    AccelerationContextTransmitter(settings.SERVER_HOST, settings.SERVER_PORT, "/api/context", -1.2, 1.2).start()