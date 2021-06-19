import urllib.parse
from django.http import HttpResponse, HttpRequest
import time


CACHE = {}  # PATH => (Response, EXPIRE)


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        path = urllib.parse.urlparse(request.path).path
        if path in CACHE and CACHE[path][1] > time.time():
            return CACHE[path][0]
        is_static = path.endswith(".css") or path.endswith(".js") or path.endswith(".html")
        response = self.get_response(request)
        if is_static:
            CACHE[path] = (response, time.time() + 10)
        return response
