import datetime
import json

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse

from ..serializers import (
    AuthSerizliser,
    RequestsTableSerializer,
    RequestsSerializer
)
from ..models import (
    RequestModel
)
from ..utils import (
    post_and_auth
)


class AuthMethods:
    @staticmethod
    def auth_page(request):
        """view for get auth page"""

        if not request.user.is_authenticated:
            return render(request, 'auth.html', context={})
        elif request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/user-page/')

    @staticmethod
    def auth(request):
        """view for user's auth"""

        if request.method != 'POST':
            print(1)
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        if request.user.is_authenticated:
            print(2)
            return JsonResponse(data={
                "error": "2"
            }, status=400)

        # get data from request
        # noinspection PyBroadException
        try:
            data = json.loads(request.body)
        except:
            data = {}

        # control validation for data
        if not AuthSerizliser(data=data).is_valid():
            print(3)
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        # to authenticate user
        print(data['login'], ' ', data['password'])
        user = authenticate(
            username=data['login'],
            password=data['password']
        )
        if user is not None:
            login(request, user)
            return JsonResponse(data={}, status=200)
        else:
            print(4)
            return JsonResponse(data={
                "error": "4"
            }, status=400)

    @staticmethod
    def exit(request):
        logout(request)
        return JsonResponse(data={}, status=200)


class UserMethods:
    @staticmethod
    def get_users_page(request):
        """get user's page"""

        if not request.user.is_authenticated:
            return redirect('/')
        elif request.user.is_superuser:
            return redirect('/admin/')
        else:
            # get all request objects
            request_objects = RequestModel.objects.all().order_by('date_creation', )

            # if request_objects is empty
            if len(request_objects) == 0:
                request_empty = True
            else:
                request_empty = False

            return render(request, 'main.html', context={
                'user': request.user,
                'requests': RequestsTableSerializer.get_data(
                    RequestsSerializer(request_objects, many=True)
                ),
                'request_empty': request_empty
            })

    @staticmethod
    def new_request_page(request):
        if request.user.is_superuser:
            return redirect('/')
        elif not request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'new_request.html')

    @staticmethod
    def new_request(request):
        if not post_and_auth(request):
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        new_request = request.POST.get('request', None)
        if new_request == '':
            return redirect('/user-new-request-page/')

        if new_request is not None:
            new_request_object = RequestModel.objects.create(
                name=str(new_request),
                date_creation=datetime.date.today(),
                status='new',
                user=request.user
            )
            new_date = str(new_request_object.date_creation)
            return redirect('/user-new-request-page/')
        else:
            return redirect('/user-new-request-page/')
