from celery import shared_task
import datetime
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel

@shared_task
def wow(id):
    request_object = RequestModel.objects.get(id=id)
    request_object.datetime_site_parsing_started = datetime.datetime.now()
    request_object.save()

    for i in ResultModel.objects.filter(request=request_object):
        i.status = True
        i.mail = 'genag4448@gmail.com'
        i.save()

    request_object.datetime_processing_finished = datetime.datetime.now()
    request_object.save()


@shared_task()
def get_csv(data):
    """parce site and send message to client"""

    # get data for working
    mail = data.get('mail')
    url = data.get('url')

    #

