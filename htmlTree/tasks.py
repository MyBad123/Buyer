from celery import shared_task
import datetime
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel

@shared_task
def wow(id):
    request_object = RequestModel.objects.get(id=id)
    request_object.datetime_site_parsing_started = datetime.datetime.now()
    request_object.save()

    for i in range(1, 5):
        google_object = ResultModel.objects.filter(
            request=request_object,
            system='google'
        )[i]
        google_object.status = True
        google_object.mail = 'genag4448@gmail.com'
        google_object.save()

        yandex_object = ResultModel.objects.filter(
            request=request_object,
            system='yandex'
        )[i]
        yandex_object.status = True
        yandex_object.mail = 'genag4448@gmail.com'
        yandex_object.save()

    request_object.datetime_processing_finished = datetime.datetime.now()
    request_object.save()



