import validators

from email_validate import validate
from django.shortcuts import render, redirect

from htmlTree.tasks import get_csv


class CsvSerializer:
    def __init__(self, request):
        self.mail = request.POST.get('mail', None)
        self.url = request.POST.get('url', None)

    def is_valid(self):
        """control type and other things of data"""

        # work with mail
        if type(self.mail) != str:
            return False

        if not validate(email_address=self.mail):
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

        # control request
        if request.method != 'POST':
            return redirect('/get-csv/')

        # control valid data
        valid_object = CsvSerializer(request)
        if valid_object.is_valid():
            get_csv.delay(
                valid_object.get_valid_data()
            )

        return redirect('/get-csv/')
