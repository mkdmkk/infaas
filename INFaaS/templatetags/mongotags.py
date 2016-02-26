from django import template

register = template.Library()


@register.filter('mongo_id')
def mongo_id(object):
    return str(object['_id'])


@register.filter('mongo_id_from_dict')
def mongo_id_from_dict(object):
    return str(object['_id']['$oid'])