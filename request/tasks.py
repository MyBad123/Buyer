from time import sleep

from celery import shared_task

from app.models import RequestModel


@shared_task
def add(id):
    sleep(10)

    request_object = RequestModel.objects.get(
        id=id
    )
    request_object.status = 'ready'
    request_object.save()



