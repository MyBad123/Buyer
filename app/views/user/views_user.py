import datetime
import json

from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.serializers import (
    AuthSerizliser,
    RequestsTableSerializer,
    RequestsSerializer
)
from app.models import (
    RequestModel, UserForCompany
)
from app.utils import (
    post_and_auth
)
from request.tasks import (
    add
)


class ForGetUsersPageApi:
    """some utils for get_users_page_api method"""

    def __init__(self, company) -> None:
        self.company = company

    @staticmethod
    def time_status(req_obj: RequestModel) -> str:
        """get status of request obj"""

        # get stage
        if req_obj.datetime_google_started is None:
            return 'в очереди'
        elif req_obj.datetime_google_finished is None:
            return 'поиск в google search начался'
        elif req_obj.datetime_google_started is None:
            return 'поиск в google search закончился'
        elif req_obj.datetime_yandex_finished is None:
            return 'поиск в yandex search начался'
        elif req_obj.datetime_site_parsing_started is None:
            return 'поиск в yandex search закончился'
        elif req_obj.datetime_processing_finished is None:
            return 'ссылки в обработке'
        else:
            return 'окончание'

    def get_status(self) -> list:
        """get list of status for requests from db"""

        status_list = []
        for i in RequestModel.objects.filter(company=self.company):
            status_list.append({
                'id': i.id,
                'status': ForGetUsersPageApi.time_status(i)
            })

        return status_list


class AuthMethods:
    @staticmethod
    def auth_page(request):
        """view for get auth page"""

        # get params from GET request
        redirect_page = request.GET.get('redirect')
        if redirect_page != None:
            redirect_page = redirect_page.replace('%2F', '/')

        if redirect_page is None:
            # get page without redirect
            if not request.user.is_authenticated:
                return render(request, 'user/auth/auth.html')
            elif request.user.is_superuser:
                return redirect('/admin/')
            else:
                return redirect('/user-page/')

        else:
            # get page with redirect
            pass

    @staticmethod
    def auth(request):
        """view for user's auth"""

        if request.method != 'POST':
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        if request.user.is_authenticated:
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
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        # to authenticate user
        user = authenticate(
            username=data['login'],
            password=data['password']
        )
        if user is not None:
            login(request, user)
            return JsonResponse(data={}, status=200)
        else:
            return JsonResponse(data={
                "error": "4"
            }, status=400)

    @staticmethod
    def exit(request):
        logout(request)
        return redirect('/')


class UserMethods:
    @staticmethod
    def get_users_page(request):
        """get user's page"""

        # control permissions for user
        if not request.user.is_authenticated:
            return redirect('/')

        if request.user.is_superuser:
            return redirect('/admin/')

        # get company for user
        company = UserForCompany.objects.get(
            user=request.user
        ).company

        # get all request objects
        request_objects = RequestModel.objects.filter(
            company=company
        )
        request_objects = request_objects.order_by(
            'datetime_created'
        )

        # if request_objects is empty
        if len(request_objects) == 0:
            request_empty = True
        else:
            request_empty = False

        return render(request, 'user/main/main.html', context={
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
            return render(request, 'user/request/new_request.html', context={
                'error_name': False,
                'error_words': False
            })

    @staticmethod
    def new_request(request):
        if not post_and_auth(request):
            return redirect('/')

        new_request = request.POST.get('request', None)
        if (new_request == '') or (type(new_request) != str):
            return render(request, 'user/request/new_request.html', context={
                'error': True,
                'error_words': False
            })

        words = request.POST.get('words', None)
        if (words == '') or (type(words) != str):
            return render(request, 'user/request/new_request.html', context={
                'error': False,
                'error_words': True
            })

        # get company
        company = UserForCompany.objects.get(
            user=request.user
        ).company

        new_request_object = RequestModel.objects.create(
            name=new_request,
            words=words,
            datetime_created=datetime.datetime.now(),
            creator=request.user,
            company=company
        )
        add.delay(new_request_object.id)

        return redirect('/user-thanks/')

    @staticmethod
    def get_users_page_api(request) -> JsonResponse:
        """get data for main page"""

        # get company
        try:
            company = UserForCompany.objects.get(
                user=request.user
            ).company
        except UserForCompany.DoesNotExist:
            return JsonResponse(data={}, status=200)
        except TypeError:
            return JsonResponse(data={}, status=200)

        # get status for all requests from db
        utils_obj = ForGetUsersPageApi(company)

        return JsonResponse(data={
            'status': utils_obj.get_status()
        }, status=200)
