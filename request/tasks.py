import requests
import datetime

from time import sleep
from celery import shared_task
from requests.auth import HTTPBasicAuth

from app.models import RequestModel, ResultModel
from htmlTree.tasks import wow


@shared_task
def add(id):
    try:
        word = RequestModel.objects.get(id=id).name
    except:
        return None

    print(1)
    # request in google search
    request_google = requests.post(
        'https://api.dataforseo.com/v3/serp/google/organic/task_post',
        auth=HTTPBasicAuth('genag4448@gmail.com', '69c67e2c2649d919'),
        data=("[ { \"language_code\": \"RU\", \"location_code\": 2643, \"priority\": \"2\", \"keyword\": \"" + word + "\" } ]").encode('utf-8')
    )
    if request_google.json().get('status_code') == 20000:
        request_google_id = request_google.json().get('tasks')[0].get('id')
    else:
        return None
    print(request_google_id)

    # request to yandex search
    request_yandex = requests.post(
        "https://api.dataforseo.com/v3/serp/yandex/organic/task_post",
        auth=HTTPBasicAuth('genag4448@gmail.com', '69c67e2c2649d919'),
        data=("[ { \"language_code\": \"RU\", \"location_code\": 2643, \"priority\": \"2\", \"keyword\": \"" + word + "\" } ]").encode('utf-8')
    )
    if request_yandex.json().get('status_code') == 20000:
        request_yandex_id = request_yandex.json().get('tasks')[0].get('id')
    else:
        return None
    print(request_yandex_id)

    # result for google and yandex
    while True:
        sleep(60)
        response_google = requests.get(
            'https://api.dataforseo.com/v3/serp/google/organic/task_get/regular/$id=' + request_google_id,
            auth=HTTPBasicAuth('genag4448@gmail.com', '69c67e2c2649d919')
        )
        if response_google.json().get('tasks')[0].get('status_code') == 20000:
            break

    print(response_google.json())

    while True:
        sleep(60)
        response_yandex = requests.get(
            'https://api.dataforseo.com/v3/serp/yandex/organic/task_get/regular/$id=' + request_yandex_id,
            auth=HTTPBasicAuth('genag4448@gmail.com', '69c67e2c2649d919')
        )
        if response_yandex.json().get('tasks')[0].get('status_code') == 20000:
            break

    print(response_yandex.json())

    # save results to db
    for i in response_google.json().get('tasks')[0].get('result')[0].get('items'):
        ResultModel.objects.create(
            request=RequestModel.objects.get(id=id),
            system='google',
            url=i.get('url')
        )

    for i in response_yandex.json().get('tasks')[0].get('result')[0].get('items'):
        ResultModel.objects.create(
            request=RequestModel.objects.get(id=id),
            system='yandex',
            url=i.get('url')
        )

    wow.delay(id)


