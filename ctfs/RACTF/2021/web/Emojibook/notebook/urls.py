"""notebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from notes import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/register', views.RegisterFormView.as_view(), name="register"),
    path('auth/', include('django.contrib.auth.urls')),
    path('new/', views.create_note, name="new"),
    path('<int:pk>/', views.view_note, name="note"),
    path('', views.home, name="home")
]
