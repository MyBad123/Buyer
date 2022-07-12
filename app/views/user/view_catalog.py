import os
import requests
import datetime
import pathlib
from django.http import FileResponse, HttpResponse
import validators
import threading

from email_validate import validate
from django.shortcuts import render, redirect

from htmlTree.tasks import get_catalog
from app.models import CsvModel


class Bg(threading.Thread):
    def __init__(self, function_that_downloads, argv1):
        threading.Thread.__init__(self)
        self.runnable = function_that_downloads
        self.daemon = True
        self.argv1 = argv1

    def run(self):
        self.runnable(self.argv1)


class CsvSerializer:
    def __init__(self, request):
        self.url = request.POST.get('url', None)

    def is_valid(self):
        """control type and other things of data"""

        # work with url
        if type(self.url) != str:
            return False

        if validators.url(self.url) is not True:
            return False

        return True

    def get_valid_data(self):
        """get dick with valid data"""

        return {
            'url': self.url
        }


class CatalogView:
    """methods for work with catalog"""

    @staticmethod
    def get_page(request):
        """get catalog page with form"""

        return render(request, 'user/catalog/catalog.html')

    @staticmethod
    def set_catalog(request):
        """get catalog from bd"""

        # control request
        if request.method != 'POST':
            return redirect('/get-csv/')

        # control valid data
        valid_object = CsvSerializer(request)
        if valid_object.is_valid():
            thread = Bg(get_catalog, valid_object.get_valid_data())
            dictionary = thread.start()
            return render(request, 'user/catalog/get_catalog.html', dictionary)
        else:
            return redirect('/get-catalog/')
