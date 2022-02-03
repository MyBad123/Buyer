from django.db import models
from django.contrib.auth.models import User


class RequestModel(models.Model):
    """Model for user's request."""

    name = models.CharField(max_length=200)
    date_creation = models.DateField()
    status = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
