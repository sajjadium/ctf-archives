from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Note(models.Model):
    name = models.CharField(max_length=255)
    body = models.TextField()
    author = models.ForeignKey(to=User, on_delete=CASCADE)
