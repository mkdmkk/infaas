import httplib2
import json

__author__ = 'Moon Kwon Kim <mkdmkk@gmail.com>'

class Communicator(object):
    def __init__(self, host, port, url):
        self.url = url
        self.conn = httplib2.HTTPConnection(host, port)

    def post(self, data):
        print("Parameters: %s" % data)
        self.conn.request("POST", self.url, json.dumps(data), headers={"Content-Type": "application/json"})
        response = self.conn.getresponse()
        print("Response: %s" % response.status)

