from django.db import models
from django.contrib.auth.models import User


class RequestModel(models.Model):
    """Model for user's request."""

    name = models.CharField(max_length=200)
    words = models.CharField(max_length=300)
    datetime_created = models.DateTimeField()
    datetime_google_started = models.DateTimeField(null=True, blank=True)
    datetime_google_finished = models.DateTimeField(null=True, blank=True)
    datetime_yandex_started = models.DateTimeField(null=True, blank=True)
    datetime_yandex_finished = models.DateTimeField(null=True, blank=True)
    datetime_site_parsing_started = models.DateTimeField(null=True, blank=True)
    datetime_processing_finished = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'requests'



class ResultModel(models.Model):
    """Models for urls of request"""

    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    system = models.CharField(max_length=20)
    url = models.TextField()

    class Meta:
        db_table = 'search_engine_results'

