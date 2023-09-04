from django.db import models

class Flag(models.Model):
    """
        Flag model
    """
    flag = models.CharField(max_length=255)

    def __str__(self) -> str:
        return "Top Secret Flag"