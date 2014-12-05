from django.template.loader_tags import register

__author__ = 'mkk'

@register.filter
def getitem(collection, string):
    return collection.get(string,'')