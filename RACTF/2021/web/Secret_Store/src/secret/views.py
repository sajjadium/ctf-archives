from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import CreateView
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from secret.models import Secret
from secret.permissions import IsSecretOwnerOrReadOnly
from secret.serializers import SecretSerializer


class SecretViewSet(viewsets.ModelViewSet):
    queryset = Secret.objects.all()
    serializer_class = SecretSerializer
    permission_classes = (IsAuthenticated & IsSecretOwnerOrReadOnly,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = "__all__"


class RegisterFormView(CreateView):
    template_name = "registration/register.html"
    form_class = UserCreationForm
    model = User
    success_url = "/"


def home(request):
    if request.user.is_authenticated:
        secret = Secret.objects.filter(owner=request.user)
        if secret:
            return render(request, "home.html", context={"secret": secret[0].value})
    return render(request, "home.html")
