import urllib.parse

from django.http import HttpRequest
from django.template import Library

register = Library()

@register.simple_tag
def query_extender(request: HttpRequest, key, value):
    dict_: dict = request.GET.copy()
    dict_[key] = value
    return "?" + urllib.parse.urlencode(dict_)
    # {'name': 'sasho', 'page:10'} => ?name=sasho&page=10