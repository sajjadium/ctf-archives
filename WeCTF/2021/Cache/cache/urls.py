import os

from django.urls import re_path
from django.http import HttpResponse, HttpRequest


FLAG = os.getenv("FLAG")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


def flag(request: HttpRequest):
    token = request.COOKIES.get("token")
    print(token, ADMIN_TOKEN)
    if not token or token != ADMIN_TOKEN:
        return HttpResponse("Only admin can view this!")
    return HttpResponse(FLAG)


def index(request: HttpRequest):
    return HttpResponse("Not thing here, check out /flag.")


urlpatterns = [
    re_path('index', index),
    re_path('flag', flag)
]
