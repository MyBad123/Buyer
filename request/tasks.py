import enum
import os
import pathlib
import uuid
import time
import zipfile
import json
import shutil

import requests
import datetime

from celery import shared_task
from django.contrib.auth.models import User

from app.models import RequestModel, ResultModel, MailForMessageModel
from htmlTree.tasks import wow

from .mail import Mail


class Params(enum.Enum):
    BEFORE_GOOGLE = 1
    AFTER_GOOGLE = 2
    BEFORE_YANDEX = 3
    AFTER_YANDEX = 4


class BatchesApiClass:
    """methods for work with batches in SerpWow"""

    def create_batch_google(self):
        body = {
            "name": "My First Batch",
            "searches_type": "google_web"
        }

        api_result = requests.post(
            'https://api.serpwow.com/live/batches?api_key=9315F7DE02AC45209E4E6EAA5DB201E0',
            json=body
        )
        return api_result.json().get('batch').get('id')

    def create_batch_yandex(self):
        body = {
            "name": "My First Batch",
            "searches_type": "yandex_web"
        }

        api_result = requests.post(
            'https://api.serpwow.com/live/batches?api_key=9315F7DE02AC45209E4E6EAA5DB201E0',
            json=body
        )
        return api_result.json().get('batch').get('id')

    def create_request_google(self, words, batch_id):
        # for google
        body = {
            "searches": [
                {
                    "q": words,
                    "custom_id": "for_google",
                    "max_page": 100,
                    'gl': 'ru',
                    'hl': 'ru',
                    'location': 'Russia',
                    'google_domain': 'google.ru',
                    'custom_id': 'this-19'
                }
            ]
        }
        requests.put(
            'https://api.serpwow.com/live/batches/' + batch_id + '?api_key=9315F7DE02AC45209E4E6EAA5DB201E0',
            json=body
        )

    def create_request_yandex(self, words, batch_id):
        body = {
            "searches": [
                {
                    "q": words,
                    "custom_id": "for_google",
                    "max_page": 100,
                    'location': 'Russia',
                    'engine': 'yandex'
                }
            ]
        }
        requests.put(
            'https://api.serpwow.com/live/batches/' + batch_id + '?api_key=9315F7DE02AC45209E4E6EAA5DB201E0',
            json=body
        )

    def start_search(self, batch_id):
        params = {
            'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0'
        }
        requests.get('https://api.serpwow.com/live/batches/' + batch_id + '/start', params)

    def stop_search(self, batch_id):
        params = {
            'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0'
        }
        requests.get('https://api.serpwow.com/live/batches/' + batch_id + '/stop', params)

    def check_status(self, batch_id):
        params = {
            'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0'
        }
        api_result = requests.get(
            'https://api.serpwow.com/live/batches/' + batch_id + '/results',
            params
        )

        return api_result.json()

    def get_url_for_download(self, batch_id, request_id):
        """get url for download from request for results"""

        params = {
            'api_key': '9315F7DE02AC45209E4E6EAA5DB201E0'
        }
        api_result = requests.get(
            'https://api.serpwow.com/live/batches/' + batch_id + '/results/' + str(request_id),
            params
        )

        return api_result.json().get('result').get('download_links').get('all_pages')


    def get_info_from_file(self, id_request, zip_url):
        """get info from download file"""

        # control folders
        path = str(pathlib.Path(__file__).parent)
        if not os.path.isdir(path + '/files'):
            os.mkdir(path + '/files')

        path += '/files/'

        # work with env for file
        path += str(id_request)
        path += '/'
        os.mkdir(path)

        # work with download file
        with open(path + '1.zip', 'wb') as file:
            download_request = requests.get(zip_url)
            file.write(download_request.content)

        data = None
        with zipfile.ZipFile(path + '1.zip') as myzip:
            for i in myzip.namelist():
                with myzip.open(i) as myfile:
                    data = myfile.read()

        # delete folders
        path = str(pathlib.Path(__file__).parent) + '/files/' + str(id_request)
        try:
            os.rmdir(path)
        except OSError:
            shutil.rmtree(path)

        return json.loads(data.decode('utf-8'))[0].get('result').get('organic_results')


class SerpClass(BatchesApiClass):
    """class for scan google and yandex"""

    def __init__(self, request_object):
        self.link_list = []
        self.request_object = request_object

    def work_with_search_system(self):
        """func for working with Google and Yandex"""

        # new batches in SerpWow
        batch_google = super().create_batch_google()
        batch_yandex = super().create_batch_yandex()

        print(1)

        # new requests in new batches
        super().create_request_yandex(self.request_object.words, batch_yandex)
        super().create_request_google(self.request_object.words, batch_google)

        print(2)

        # start work in batches
        super().start_search(batch_yandex)
        super().start_search(batch_google)

        # get results from searching(google)
        self.set_status(Params.BEFORE_GOOGLE)

        for_while = True
        while for_while:
            try:
                for_results = super().check_status(batch_google)
                if len(for_results.get('results')) != 0:
                    results_id = for_results.get('results')[0].get('id')
                    for_while = False
                else:
                    time.sleep(150)

                print(4)
            except KeyError:
                pass

        url_file = super().get_url_for_download(batch_google, results_id)
        for i in super().get_info_from_file(self.request_object.id, url_file):
            ResultModel.objects.create(
                request=self.request_object,
                system='google',
                url=i.get('link')
            )

        print(5)

        self.set_status(Params.AFTER_GOOGLE)

        # get results from searching(yandex)
        self.set_status(Params.BEFORE_YANDEX)
        time.sleep(600)

        for_while = True
        while for_while:
            try:
                for_results = super().check_status(batch_yandex)
                if len(for_results.get('results')) != 0:
                    results_id = for_results.get('results')[0].get('id')
                    for_while = False
                else:
                    time.sleep(300)
            except KeyError:
                pass

        url_file = super().get_url_for_download(batch_yandex, results_id)
        for i in super().get_info_from_file(self.request_object.id, url_file):
            ResultModel.objects.create(
                request=self.request_object,
                system='yandex',
                url=i.get('link')
            )
        self.set_status(Params.AFTER_YANDEX)

        # delete batches
        requests.delete(
            'https://api.serpwow.com/live/batches/' + batch_google + '?api_key=9315F7DE02AC45209E4E6EAA5DB201E0'
        )
        requests.delete(
            'https://api.serpwow.com/live/batches/' + batch_yandex + '?api_key=9315F7DE02AC45209E4E6EAA5DB201E0'
        )

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

    print(data)

    # update user in date
    user_object = User.objects.get(id=data.get('user'))
    data.update({
        'user': user_object
    })

    mails_list = []
    for i in data.get('chats'):
        try:
            mail_obj = MailForMessageModel.objects.get(id=i)
            mails_list.append(mail_obj)
        except MailForMessageModel.DoesNotExist:
            pass

    mail_object = Mail(
        text=data.get('text'),
        request_id=data.get('request_id')
    )
    mail_object.send_mails(
        mails=mails_list,
        user=data.get('user')
    )


@shared_task
def send_marcup_csv_attach(email, url):
    uuid4 = uuid.uuid4()
    parser = Parser()
    parser.site_parsing(url, uuid4, None)
    csv_path = parser_path + f'/csv_results/{uuid4}.csv'
    Mail.send_email_attach(email, csv_path)
    os.remove(csv_path)