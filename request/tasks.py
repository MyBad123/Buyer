from pydoc import text
import requests
import datetime

from time import sleep
from celery import shared_task
from requests.auth import HTTPBasicAuth
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel
from htmlTree.tasks import wow

from .mail import Mail


class WorkWithDataForSeo:
    def __init__(self, request_object):
        self.response_yandex = None
        self.response_google = None
        self.request_yandex_id = None
        self.request_google_id = None
        self.request_object = request_object

    def change_datetime(self, datetime_status):
        """write time for stage"""

        if datetime_status == 'datetime_google_started':
            self.request_object.datetime_google_started = datetime.datetime.now()
            self.request_object.save()
        if datetime_status == 'datetime_google_finished':
            self.request_object.datetime_google_finished = datetime.datetime.now()
            self.request_object.save()
        if datetime_status == 'datetime_yandex_started':
            self.request_object.datetime_yandex_started = datetime.datetime.now()
            self.request_object.save()
        if datetime_status == 'datetime_yandex_finished':
            self.request_object.datetime_yandex_finished = datetime.datetime.now()
            self.request_object.save()

    def request_to_google(self):
        """make request for DataForSeo(google serach)"""

        self.change_datetime('datetime_google_started')

        request_google = requests.post(
            'https://api.dataforseo.com/v3/serp/google/organic/task_post',
            auth=HTTPBasicAuth('9228793@gmail.com', 'd08dd8eaf28be140'),
            data=("[ { \"language_code\": \"RU\", \"location_code\": 2643, \"priority\": \"2\", \"keyword\": \"" + self.request_object.words + "\" } ]").encode('utf-8')
        )
        if request_google.json().get('status_code') == 20000:
            self.request_google_id = request_google.json().get('tasks')[0].get('id')
        else:
            return False

        return True

    def request_to_yandex(self):
        """make request for DataForSeo(yandex search)"""

        self.change_datetime('datetime_yandex_started')

        request_yandex = requests.post(
            "https://api.dataforseo.com/v3/serp/yandex/organic/task_post",
            auth=HTTPBasicAuth('9228793@gmail.com', 'd08dd8eaf28be140'),
            data=("[ { \"language_code\": \"RU\", \"location_code\": 2643, \"priority\": \"2\", \"keyword\": \"" + self.request_object.words + "\" } ]").encode('utf-8')
        )
        if request_yandex.json().get('status_code') == 20000:
            self.request_yandex_id = request_yandex.json().get('tasks')[0].get('id')
        else:
            return False

        return True

    def get_google_results(self):
        """get urls from google search"""

        while True:
            sleep(60)
            self.response_google = requests.get(
                'https://api.dataforseo.com/v3/serp/google/organic/task_get/regular/$id=' + self.request_google_id,
                auth=HTTPBasicAuth('9228793@gmail.com', 'd08dd8eaf28be140')
            )
            if self.response_google.json().get('tasks')[0].get('status_code') == 20000:
                break

    def get_yandex_results(self):
        """get urls from yandex search"""

        while True:
            sleep(60)
            self.response_yandex = requests.get(
                'https://api.dataforseo.com/v3/serp/yandex/organic/task_get/regular/$id=' + self.request_yandex_id,
                auth=HTTPBasicAuth('9228793@gmail.com', 'd08dd8eaf28be140')
            )
            if self.response_yandex.json().get('tasks')[0].get('status_code') == 20000:
                break

    def write_results_to_db_google(self):
        for_index = 0
        for i in self.response_google.json().get('tasks')[0].get('result')[0].get('items'):

            if for_index == 10:
                break
            else:
                for_index += 1

            ResultModel.objects.create(
                request=self.request_object,
                system='google',
                url=i.get('url')
            )

        self.change_datetime('datetime_google_finished')

    def write_results_to_db_yandex(self):
        for_index = 0
        for i in self.response_yandex.json().get('tasks')[0].get('result')[0].get('items'):

            if for_index == 10:
                break
            else:
                for_index += 1

            ResultModel.objects.create(
                request=self.request_object,
                system='yandex',
                url=i.get('url')
            )

        self.change_datetime('datetime_yandex_finished')


@shared_task
def add(id_object):
    try:
        request_object = RequestModel.objects.get(id=id_object)
    except RequestModel.DoesNotExist:
        return None

    # class_search = WorkWithDataForSeo(request_object)

    # work with google search
    # class_search.request_to_google()
    # class_search.get_google_results()
    # class_search.write_results_to_db_google()

    # work with yandex search
    # class_search.request_to_yandex()
    # class_search.get_yandex_results()
    # class_search.write_results_to_db_yandex()

    list_refs = [
        'https://taxibox.ru/models/reklamniy-svetovoi-korob-na-taksi-big-1000.html',
        'https://exomenu.ru/python10/',
        'https://www.tangleteezer.ru/all-brushes/hairspray/detangling-sprays/detangling-spray-for-kids/',
        'https://nskshapki.ru/catalog/product/id/3851/',
        'https://belobuv.ru/wl-1e-inblu-krossovki-zhenskie.html'
    ]    
    index_system = 0

    for i in list_refs:
        index_system += 1
        
        if (index_system % 2):
            ResultModel.objects.create(
                request=request_object,
                system='yandex',
                url=i
            )
        else:
            ResultModel.objects.create(
                request=request_object,
                system='google',
                url=i
            )

    request_object.datetime_google_started = datetime.datetime.now()
    request_object.save()
    sleep(10)

    request_object.datetime_google_finished = datetime.datetime.now()
    request_object.save()
    sleep(10)

    request_object.datetime_yandex_started = datetime.datetime.now()
    request_object.save()
    sleep(10)

    request_object.datetime_yandex_finished = datetime.datetime.now()
    request_object.save()

    wow.delay(id_object)


@shared_task
def send(data: dict):
    """func for sending mails"""

    # update user in date
    user_object = User.objects.get(id=data.get('user'))
    data.update({
        'user': user_object
    })

    mail_object = Mail(
        text=data.get('text'),
        request_id=data.get('request_id')
    )
    mail_object.send_mails(
        mails=data.get('mails'),
        user=data.get('user')
    )
