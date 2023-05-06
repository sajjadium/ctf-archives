from django.conf.urls import url
from .views import ColorsView, HatsView

urlpatterns = [
    url(r'^hats/$', HatsView.as_view(), name='hats'),
    url(r'^colors/$', ColorsView.as_view(), name='colors'),
]
