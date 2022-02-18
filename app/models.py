from django.db import models
from django.contrib.auth.models import User


class RequestModel(models.Model):
    """Model for user's request."""

    name = models.CharField(max_length=200)
    datetime_on_search = models.DateTimeField(null=True, blank=True)
    datetime_on_tree = models.DateTimeField(null=True, blank=True)
    datetime_on_finish = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'request'


class ResultModel(models.Model):
    """Models for urls of request"""

    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    system = models.CharField(max_length=20)
    url = models.CharField(max_length=300)

