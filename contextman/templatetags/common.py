import json
from bson import json_util
from django import template
import pymongo
import copy

__author__ = 'mkk'

register = template.Library()

@register.filter
def getitem(collection, string):
    return collection.get(string,'')

@register.filter
def tostring(data):
    print("[filter.common] tostring %s" % data)
    if type(data) is pymongo.cursor.Cursor:
        clone = copy.copy(data)
        return json_util.dumps(clone).encode("utf-8")
    else:
        return json.dumps(data).encode("utf-8")
    return None

@register.filter
def encode(data, type):
    print("[filter.common] encode %s %s" % (data, type))
    return data.encode(type)