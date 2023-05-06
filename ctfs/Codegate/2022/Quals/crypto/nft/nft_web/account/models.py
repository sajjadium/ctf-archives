from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.CharField(max_length=128)
    user_pw = models.CharField(max_length=128)
    token = models.CharField(max_length=512)
    token_key = models.CharField(max_length=512)
    is_cached = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id
