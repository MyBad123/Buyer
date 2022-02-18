from celery import shared_task
import datetime
from django.contrib.auth.models import User

from app.models import RequestModel

@shared_task
def wow(id):
    request_object = RequestModel.objects.get(id=id)
    request_object.datetime_on_tree = datetime.datetime.now()
    request_object.save()

