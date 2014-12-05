from datetime import datetime
from contextman import ContextTransmitter
from INFaaS import settings

__author__ = 'mkk'

if __name__ == "__main__":

    context_transmitter = ContextTransmitter(settings.SERVER_HOST, settings.SERVER_PORT, "/context")

    f = open('./WISDM_ar_v1.1_raw.txt', 'r')
    for line in f:
        values_str = line.split(';')[0]
        values = values_str.split(',')
        if len(values) >= 6:
            context = {}
            context["source"] = 2
            context["type"] = "acceleration"
            context["time"] = values[2]
            context["data"] = {}
            context["data"]["x"] = values[3]
            context["data"]["y"] = values[4]
            context["data"]["z"] = values[5]
            context_transmitter.post(context)