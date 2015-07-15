import calendar
import json
import os
import threading
import urlparse
from django.http import HttpResponse
import math
from INFaaS import settings
from contextman import contextman, contexttypes

__author__ = 'mkk'

import oauth2 as oauth
import httplib2
import time

"""
Types of Withings Measurements
1 : Weight (kg)
4 : Height (meter)
5 : Fat Free Mass (kg)
6 : Fat Ratio (%)
8 : Fat Mass Weight (kg)
9 : Diastolic Blood Pressure (mmHg)
10 : Systolic Blood Pressure (mmHg)
11 : Heart Pulse (bpm)
54 : SP02(%)
"""
WITHINS_MEAS_TYPES = {
    1: contexttypes.WEIGHT,
    4: contexttypes.HEIGHT,
    8: contexttypes.FAT,
    9: contexttypes.DIASTOLIC,
    10: contexttypes.SYSTOLIC,
    11: contexttypes.PULSE,
    54: contexttypes.SPO2
}

class WithingsAcquisition(threading.Thread):

    instance = None
    CACHE_PATH = ".cache/oauth2/cache"

    __slots__ = [
        'consumer_key',
        'consumer_secret',
        'request_token_url',
        'authorize_url',
        'access_token_url',
        'api_url',
        'callback_url',
        'userid',
        'consumer',
        'client',
        'request_token',
        'access_token',
        'oauth_verifier'
    ]

    def __init__(self, consumer_key=None, consumer_secret=None, acquisition_interval=3600):
        threading.Thread.__init__(self)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.request_token_url = 'https://oauth.withings.com/account/request_token'
        self.authorize_url = 'http://oauth.withings.com/account/authorize'
        self.access_token_url = 'http://oauth.withings.com/account/access_token'
        self.api_url = 'http://wbsapi.withings.net/measure'
        self.callback_url = 'http://%s:%s/cb/acquisition/withings' % (settings.SERVER_HOST, settings.SERVER_PORT)

        self.request_token_url += "?oauth_callback=%s" % self.callback_url
        self.consumer = oauth.Consumer(self.consumer_key, self.consumer_secret)
        self.client = oauth.Client(self.consumer)

        self.cm = contextman.ContextManager()

        self.acquisition_interval = acquisition_interval
        WithingsAcquisition.instance = self


    def connect(self, cache=False):
        if not os.path.isfile(os.path.join(settings.BASE_DIR, WithingsAcquisition.CACHE_PATH)) or cache == False:
            if self._request_token():
                self._authorize()
            else:
                print("[WithingsAcquisition] Connection Failed.")
        else:
            with open(WithingsAcquisition.CACHE_PATH, "r") as f:
                time = f.readline()
                conf = f.readline()
            if time != "" and conf != "":
                time = int(time)
                conf = json.loads(conf)
                self.request_token = conf["request_token"]
                self.userid = conf["userid"]
                self.access_token = conf["access_token"]
                self.oauth_verifier = conf["oauth_verifier"]
            if self._access():
                self.start()


    def run(self):
        while True:
            self._acquire()
            time.sleep(self.acquisition_interval)


    def _request_token(self):
        """
        Step 1. Request Token
        :return:
        """
        resp, content = self.client.request(self.request_token_url, "GET")
        print("[Request Token] Response: %s" % resp)
        if resp['status'] != '200':
            raise Exception("[Request Token] Invalid response %s." % resp['status'])
        self.request_token = dict(urlparse.parse_qsl(content)) # return list of name/value pairs
        if "oauth_token" in self.request_token and "oauth_token_secret" in self.request_token:
            print("[Request Token] Content:")
            print("\t- oauth_token\t= %s" % self.request_token['oauth_token'])
            print("\t- oauth_token_secret\t= %s" % self.request_token['oauth_token_secret'] if "oauth_token_secret" in self.request_token else "None")
        else:
            return False

        return True


    def _authorize(self):
        """
        Step 2. End-User Authorization
        :return:
        """
        print("[End-User Authorization] Go to the following link in your browser:")
        print("\t- %s?oauth_token=%s" % (self.authorize_url, self.request_token['oauth_token']))
        # accepted = 'n'
        # while accepted.lower() == 'n':
        #     accepted = raw_input('\t- Have you authorized me? (y/n) ')
        # self.oauth_verifier = raw_input('\t- What is the PIN? ')


    def _access(self):
        """
        Step 3. Access Token
        :return:
        """
        token = oauth.Token(self.request_token['oauth_token'], self.request_token['oauth_token_secret'])
        token.set_verifier(self.oauth_verifier)
        self.client = oauth.Client(self.consumer, token)
        resp, content = self.client.request(self.access_token_url, "POST")
        self.access_token = dict(urlparse.parse_qsl(content))
        print("[Access Token] Content: %s" % self.access_token)
        # print("\t- oauth_token\t= %s" % self.access_token['oauth_token'])
        # print("\t- oauth_token_secret\t= %s" % self.access_token['oauth_token_secret'])

        if "oauth_token" in self.access_token and "oauth_token_secret" in self.access_token:
            token = oauth.Token(self.access_token['oauth_token'], self.access_token['oauth_token_secret'])
            self.client = oauth.Client(self.consumer, token)
        else:
            self.connect(cache=False)
            return False

        return True


    def _acquire(self):
        """http://wbsapi.withings.net/measure?
        action=getmeas&
        oauth_consumer_key=f853b4e9edc1fc75e367fbb60c1b5ff2833b16e2d34d3d5f99055bb560d&
        oauth_nonce=3ac21b822f84682a218493a918e444b0&
        oauth_signature=0xmUGyijFV348S1Qf9E32sc2ySE%3D&
        oauth_signature_method=HMAC-SHA1&
        oauth_timestamp=1430466875&d
        oauth_token=&
        oauth_version=1.0&
        userid="""

        try:
            result = self.cm.retrieve(sort_key="time", sort_order="desc", limit=1)
            if result is not None and result.count() > 0:
                startdate = calendar.timegm(time.strptime(result[0]['time'], settings.TIME_FORMAT))+1
            else:
                startdate = 0

            h = httplib2.Http(".cache/httplib2")
            request_url = self.api_url+\
                          "?action=%s&" \
                          "userid=%s&" \
                          "startdate=%s" % ('getmeas', self.userid, startdate)
            resp, content = self.client.request(request_url, "GET")
            content = json.loads(content)
            print("[Acquire] Request URL: %s" % request_url)
            print("[Acquire] Contexts (from the date, %s):" % startdate)
            print("%s" % content)

            self.cache()
            self.sync(content)
        except:
            print("[Acquire] Error. Please check your db.")


    def sync(self, contexts):
        for g in contexts["body"]["measuregrps"]:
            date = time.strftime(settings.TIME_FORMAT, time.gmtime(int(g["date"])))
            for m in g["measures"]:
                if m["type"] in WITHINS_MEAS_TYPES:
                    type = WITHINS_MEAS_TYPES[m["type"]]
                else:
                    continue
                value = float(m["value"]) * math.pow(10, int(m["unit"]))
                print("{time: %s,\ttype: %s,\t\tvalue: %s" % (date, type, str(value)))
                self.cm.insert({"time":date, "type": type, "value":value})


    def cache(self):
        with open(WithingsAcquisition.CACHE_PATH, 'w+') as f:
            f.write("%s\n" % str(int(time.time())))
            f.write("%s" %
                    json.dumps({"request_token": self.request_token,
                     "oauth_verifier": self.oauth_verifier,
                     "userid": self.userid,
                     "access_token": self.access_token}))
            f.close()


def on_authorized(request):
    """
    Callback method called by Withings
    :param request:
    Example of request.GET: userid=6480030&oauth_token=b07b4618eec3dc99415742361b6f650b115c720b48e56dfdc99502172dcd71e&oauth_verifier=5lHBhhVT1iCc34
    :return:
    """
    WithingsAcquisition.instance.oauth_verifier = request.GET['oauth_verifier']
    WithingsAcquisition.instance.userid = request.GET['userid']
    print("[On Authorized] Content:")
    print("\t- oauth_verifier\t= %s" % WithingsAcquisition.instance.oauth_verifier)
    print("\t- userid\t= %s" % WithingsAcquisition.instance.userid)
    WithingsAcquisition.instance._access()
    WithingsAcquisition.instance.start()
    return HttpResponse("OK")