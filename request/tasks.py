import json
import enum
import requests
import datetime

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
        self.request_object = request_object

    def work_with_search_system(self):
        """func for working with Google and Yandex"""

        # part for Google
        self.set_status(Params.BEFORE_GOOGLE)

        params = {
            'api_key': '69A93F783D8E4195ACA16DA1E871C21E',
            'q': self.request_object.words,
            'gl': 'ru',
            'hl': 'ru',
            'location': 'Russia',
            'google_domain': 'google.ru',
            'num': '20'
        }
        api_result = requests.get('https://api.serpwow.com/search', params)

        # save google results
        for i in api_result.json()['organic_results']:
            ResultModel.objects.create(
                request=self.request_object,
                system='google',
                url=i.get('link')
            )
        self.set_status(Params.AFTER_GOOGLE)

        # part for Yandex
        self.set_status(Params.BEFORE_YANDEX)
        for i in range(1, 2):
            params = {
                'api_key': '69A93F783D8E4195ACA16DA1E871C21E',
                'q': self.request_object.words,
                'engine': 'yandex',
                'yandex_location': '225',
                'page': i
            }
            api_result = requests.get('https://api.serpwow.com/search', params)

            # save yandex results
            for i in api_result.json()['organic_results']:
                ResultModel.objects.create(
                    request=self.request_object,
                    system='yandex',
                    url=i.get('link')
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
