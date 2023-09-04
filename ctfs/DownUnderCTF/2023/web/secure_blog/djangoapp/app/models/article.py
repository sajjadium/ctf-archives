from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    """
        Test Article model
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}-{self.created_by.username}"
    
    class Meta:
        ordering = ["title"]