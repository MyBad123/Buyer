from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    """model for company"""

    name = models.CharField(max_length=300)


class UserForCompany(models.Model):
    """model for link of user with company"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


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
    delete_status = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        db_table = 'requests'


class ResultModel(models.Model):
    """Models for urls of request"""

    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    system = models.CharField(max_length=20)
    url = models.TextField()
    status = models.BooleanField(default=False)
    mail = models.EmailField(null=True, blank=True, default=None)

    class Meta:
        db_table = 'search_engine_results'


class MessageModel(models.Model):
    """Model for email message with company"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mail = models.EmailField()
    datetime = models.DateTimeField()
    route = models.CharField(max_length=20)
    message = models.TextField()
    number = models.CharField(max_length=50, null=True, blank=True)

    # for chats
    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)

    class Meta:
        db_table = 'messages'
        ordering = ['user', 'datetime']


class MailForMessageModel(models.Model):
    """for message id"""

    mail = models.EmailField()
    request = models.ForeignKey(RequestModel, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'mails'
        ordering = ['mail']
