import datetime
import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .serializers import (
    AuthSerizliser,
    UpdateSerialize,
    DeleteSerializer,
    RequestsTableSerializer,
    RequestsSerializer
)
from .models import (
    RequestModel
)
from .utils import (
    post_and_auth
)


class AdminMethods:
    @staticmethod
    def get_admin_page(request):
        """get admin page"""

        users = User.objects.all().exclude(username='gena').order_by('id').filter(is_superuser=False)
        print(request.user)
        if request.user.is_superuser:
            return render(request, 'admin.html', context={
                'users': users
            })
        elif not request.user.is_authenticated:
            return redirect('/')
        else:
            redirect('/app/user-page/')

    @staticmethod
    def get_new_user_page(request):
        if request.user.is_superuser:
            return render(request, 'new_user.html')
        else:
            return redirect("/app/user-page/")

    @staticmethod
    def new_user(request):
        """add new user in db"""

        if not post_and_auth(request):
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        # get data from request
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

        # control unique login
        len_users = len(
            User.objects.filter(username=data.get('login'))
        )
        if len_users != 0:
            return JsonResponse(data={
                "error": "4"
            }, status=400)

        User.objects.create_user(
            username=data.get('login'),
            password=data.get('password')
        )
        return JsonResponse(data={}, status=200)

    @staticmethod
    def update_user_page(request):
        try:
            user = User.objects.get(id=int(request.GET.get('id', 0)))
        except:
            return redirect('/app/admin/')

        if user.is_superuser:
            return redirect('/app/admin/')

        if request.user.is_superuser:
            return render(request, 'update_user.html', context={
                "login": user.username
            })
        else:
            return redirect('/app/admin/')

    @staticmethod
    def update_user(request):
        if not post_and_auth(request):
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        # get data from request
        try:
            data = json.loads(request.body)
        except:
            data = {}

        # control validation for data
        if not UpdateSerialize(data=data).is_valid():
            print(3)
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        if data['old_name'] == data['new_name']:
            user_object = User.objects.get(username=data.get('old_name'))
            user_object.set_password(data.get('password'))
            user_object.save()
        else:
            len_objects = len(User.objects.filter(username=data['new_name']))
            if len_objects != 0:
                return JsonResponse(data={
                    "error": "4"
                }, status=400)
            else:
                user_object = User.objects.get(username=data.get('old_name'))
                user_object.username = data.get('new_name')
                user_object.set_password(data.get('password'))
                user_object.save()

        return JsonResponse(data={}, status=200)

    @staticmethod
    def delete_user(request):
        if request.method != 'POST':
            print(1)
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        if not request.user.is_superuser:
            print(2)
            return JsonResponse(data={
                "error": "2"
            }, status=400)

        # get data from request
        try:
            data = json.loads(request.body)
        except:
            data = {}

        # serialize data
        if not DeleteSerializer(data=data).is_valid():
            print(3)
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        # delete data from db
        for i in User.objects.filter(username=data.get('login')):
            i.delete()

        return JsonResponse(data={}, status=200)


class DbMethods:
    @staticmethod
    def get_db_page(request):
        return render(request, 'db.html')

    @staticmethod
    def delete(request):
        for i in User.objects.all():
            i.delete()
        for i in Session.objects.all():
            i.delete()

        return JsonResponse(data={}, status=200)

    @staticmethod
    def create(request):
        if request.method != 'POST':
            return JsonResponse(data={
                'error': '1'
            })

        # get data from request
        try:
            data = json.loads(request.body)
        except:
            data = {}

        if not AuthSerizliser(data=data).is_valid():
            return JsonResponse(data={
                'error': '2'
            })

        # delete data
        for i in User.objects.all():
            i.delete()
        for i in Session.objects.all():
            i.delete()

        User.objects.create_superuser(
            username=data.get('login'),
            email=data.get('login') + '@gmail.com',
            password=data.get('password')
        )

        for i in range(0, 500):
            User.objects.create_user(
                username=str(i) + '@gmail.com',
                password=str(i)
            )
        return JsonResponse(data={}, status=200)


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

            return render(request, 'main.html', context={
                'user': request.user,
                'requests': RequestsTableSerializer.get_data(
                    RequestsSerializer(request_objects, many=True)
                )
            })

    @staticmethod
    def new_request(request):
        if not post_and_auth(request):
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        try:
            data = json.loads(request.body)
        except:
            data = {}

        if data.get('request', None) is not None:
            new_request_object = RequestModel.objects.create(
                name=str(data.get('request')),
                date_creation=datetime.date.today(),
                status='new',
                user=request.user
            )
            new_date = str(new_request_object.date_creation)
            return JsonResponse(data={
                'name': new_request_object.name,
                'date_creation': f'{ new_date[8:10]}.{ new_date[5:7] }.{ new_date[0:4] }',
                'status': new_request_object.status,
                'user': new_request_object.user.username
            }, status=200)
        else:
            return JsonResponse(data={
                "error": "2"
            }, status=400)
