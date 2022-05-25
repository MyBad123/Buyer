import os
import requests
import datetime
import pathlib
from django.http import FileResponse, HttpResponse
import validators
import threading

from email_validate import validate
from django.shortcuts import render, redirect

from htmlTree.tasks import get_csv
from app.models import CsvModel


class Bg(threading.Thread):
    def __init__(self, function_that_downloads, argv1, argv2):
        threading.Thread.__init__(self)
        self.runnable = function_that_downloads
        self.daemon = True
        self.argv1 = argv1
        self.argv2 = argv2

    def run(self):
        self.runnable(self.argv1, self.argv2)


class CsvSerializer:
    def __init__(self, request):
        self.mail = request.POST.get('mail', None)
        self.url = request.POST.get('url', None)

    def is_valid(self):
        """control type and other things of data"""

        # work with mail
        if type(self.mail) != str:
            return False

        if not validate(email_address=self.mail, check_blacklist=False):
            return False

        # work with url
        if type(self.url) != str:
            return False

        if validators.url(self.url) is not True:
            return False

        return True

    def get_valid_data(self):
        """get dick with valid data"""

        return {
            'mail': self.mail,
            'url': self.url
        }


class CsvView:
    """methods for work with csv"""

    @staticmethod
    def get_page(request):
        """get page with form"""

        return render(request, 'user/csv/csv.html')

    @staticmethod
    def set_csv(request):
        """parce site and send mail from celery"""

        # create logs
        requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=start')

        # control request
        if request.method != 'POST':
            requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=error-sev-csv-error-control-request')
            return redirect('/get-csv/')

        # get id for path
        csv_model = CsvModel.objects.create(
            datetime=datetime.datetime.now()
        )

        # control valid data
        valid_object = CsvSerializer(request)
        if valid_object.is_valid():
            thread = Bg(get_csv, valid_object.get_valid_data(), csv_model.id)
            thread.start()
        else:
            requests.get('https://buyerdev.1d61.com/set-csv-logs/?message=error-sev-csv-no-valid')

        return redirect('/get-csv/')

    @staticmethod
    def get_logs(request):
        """method for getting logs file"""

        # create path
        path = str(pathlib.Path(__file__).parent)
        path += '/pars_log.txt'

        return FileResponse(open(path, 'rb'))

    @staticmethod
    def set_logs(request):
        """method for settings logs"""

        path = str(pathlib.Path(__file__).parent)
        path += '/pars_log.txt'

        if request.GET.get('message') == 'start':
            with open(path, 'a') as file:
                file.write('\n\n\n\n\n\n')

        if request.GET.get('message', None) != None:
            with open(path, 'a') as file:
                file.write(
                    '\n' +
                    str(datetime.datetime.now()) +
                    ' ' +
                    request.GET.get('message')
                )

        return HttpResponse()
