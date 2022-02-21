from django.shortcuts import (
    render,
    redirect
)
from django.

class RequestOneView:
    @staticmethod
    def no_request_redirect(request):
        return redirect('/')

    @staticmethod
    def get_request(request, id):
        # get object
        return
