import os
from celery import shared_task
import requests
import datetime
import pathlib
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel
from .for_task_utils import Mail


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


def get_csv(data, csv_model_id):
    """parce site and send message to client"""

    # get data for working
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-start')
    mail = data.get('mail')
    url = data.get('url')

    # create path for csv file
    path_name = str(pathlib.Path(__file__).parent) + '/files/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    path_name += str(csv_model_id) + '/'
    if not os.path.exists(path_name):
        os.mkdir(path_name)

    # send message about starting
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-before-start-mail')
    mail_object = Mail(mail, path_name)
    mail_object.send_start_mail()
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-after-start-mail')

    # work with lib
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-before-rapce')
    from .ParseLib.parser_starting import start
    path_obj = start(path_name, url)
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-after-rapce')

    # send file to
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-before-end-mail')
    mail_object.send_file_mail(path_obj)
    requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=get-csv-after-end-mail')
