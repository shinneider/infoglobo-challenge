
from importlib import import_module
from inspect import isfunction
from flask_restful import Resource

def check_url_tuple(url):
    if not isinstance(url, tuple):
        raise Exception(
            "Urls inside `urlpatterns`. need to be a `tuple`"
        )

    if len(url) < 2 or not isinstance(url[0], str):
        raise Exception(
            "Not valid `urlpatterns`. All tuple need two params `url path` " +
            "and `api function`"
        )


def include(arg):
    mod = import_module(arg)

    patterns = getattr(mod, 'urlpatterns', None)
    if not patterns:
        return []
    
    if not isinstance(patterns, list):
        raise Exception(
            f" `urlpatterns` most be a list"
        )

    urls = []
    for url in patterns:
        check_url_tuple(url)

        if isinstance(url[1], list):
            for url_obj in url[1]:
                check_url_tuple(url_obj)
                url_obj = list(url_obj)
                url_obj[0] = url[0] + url_obj[0] 
                urls.append(tuple(url_obj))
        
        else:
            urls.append(url)

    return urls