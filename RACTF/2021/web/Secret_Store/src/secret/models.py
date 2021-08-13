from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Secret(models.Model):
    value = models.CharField(max_length=255)
    owner = models.OneToOneField(User, on_delete=CASCADE)
    last_updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
