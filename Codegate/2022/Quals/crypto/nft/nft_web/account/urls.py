from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('regist', views.regist, name='regist'),
    path('logout', views.logout, name='logout'),
    path('<str:user_id>/nfts/', views.nfts, name='nfts'),
]
