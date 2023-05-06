from django.conf.urls import include, url

urlpatterns = [
    url(r'^tf/', include('tf.urls', namespace='tf')),
]
