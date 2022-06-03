import enum
import os
import uuid

import requests
import datetime
import dramatiq

from celery import shared_task
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel
from htmlTree.tasks import wow

from .mail import Mail


class Params(enum.Enum):
    BEFORE_GOOGLE = 1
    AFTER_GOOGLE = 2
    BEFORE_YANDEX = 3
    AFTER_YANDEX = 4


class SerpClass:
    """class for scan google and yandex"""

    def __init__(self, request_object):
        self.link_list = []
        self.request_object = request_object

    def test_work_with_search_system(self):
        """without serpwow"""

        self.set_status(Params.BEFORE_GOOGLE)

        for i in range(1, 20):
            ResultModel.objects.create(
                request=self.request_object,
                system='google',
                url='vk.com'
            )
            ResultModel.objects.create(
                request=self.request_object,
                system='yandex',
                url='vk.com'
            )

        self.set_status(Params.AFTER_GOOGLE)
        self.set_status(Params.BEFORE_YANDEX)
        self.set_status(Params.AFTER_YANDEX)

    def work_with_search_system(self):
        """func for working with Google and Yandex"""

        # part for Google
        self.set_status(Params.BEFORE_GOOGLE)

        params = {
            'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0',
            'q': self.request_object.words,
            'gl': 'ru',
            'hl': 'ru',
            'location': 'Russia',
            'google_domain': 'google.ru',
            'num': '1000'
        }
        api_result = requests.get('https://api.serpwow.com/search', params)

        # save google results
        google_results = api_result.json()
        for i in google_results['organic_results']:
            if i.get('link') not in self.link_list:
                self.link_list.append(i.get('link'))
                if 'google' not in i.get('link'):
                    ResultModel.objects.create(
                        request=self.request_object,
                        system='google',
                        url=i.get('link')
                    )
        self.set_status(Params.AFTER_GOOGLE)

        # part for Yandex
        self.set_status(Params.BEFORE_YANDEX)
        for i in range(1, 25):
            params = {
                'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0',
                'q': self.request_object.words,
                'engine': 'yandex',
                'yandex_location': '225',
                'page': i
            }
            api_result = requests.get('https://api.serpwow.com/search', params)

            # save yandex results
            for j in api_result.json()['organic_results']:
                if j.get('link') not in self.link_list:
                    if 'yandex.ru' not in j.get('link'):
                        ResultModel.objects.create(
                            request=self.request_object,
                            system='yandex',
                            url=j.get('link')
                        )
        self.set_status(Params.AFTER_YANDEX)

    def set_status(self, param):
        """set status for request_object"""

        if param == Params.BEFORE_GOOGLE:
            self.request_object.datetime_google_started = datetime.datetime.now()
            self.request_object.save()
        elif param == Params.AFTER_GOOGLE:
            self.request_object.datetime_google_finished = datetime.datetime.now()
            self.request_object.save()
        elif param == Params.BEFORE_YANDEX:
            self.request_object.datetime_yandex_started = datetime.datetime.now()
            self.request_object.save()
        elif param == Params.AFTER_YANDEX:
            self.request_object.datetime_yandex_finished = datetime.datetime.now()
            self.request_object.save()
        else:
            pass


@shared_task
def add(id_object):
    # get request object
    try:
        request_object = RequestModel.objects.get(id=id_object)
    except RequestModel.DoesNotExist:
        return None

    # get results from google(yandex) search
    serp_object = SerpClass(request_object)
    serp_object.work_with_search_system()

    wow.delay(id_object)


@dramatiq.actor
def new_add(id_object):
    # get request object
    try:
        request_object = RequestModel.objects.get(id=id_object)
    except RequestModel.DoesNotExist:
        return None

    # get results from google(yandex) search
    serp_object = SerpClass(request_object)
    serp_object.work_with_search_system()

    request_object.datetime_site_parsing_started = datetime.datetime.now()

    for i in ResultModel.objects.filter(request=request_object):
        i.status = True
        i.mail = 'genag4448@gmail.com'
        i.save()

    request_object.datetime_processing_finished = datetime.datetime.now()
    request_object.save()


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


@shared_task
def send_marcup_csv_attach(email, url):
    uuid4 = uuid.uuid4()
    parser = Parser()
    parser.site_parsing(url, uuid4)
    csv_path = parser_path + f'/csv_results/{uuid4}.csv'
    Mail.send_email_attach(email, csv_path)
    os.remove(csv_path)