import json

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.serializers import (
    AuthSerizliser,
    UpdateSerialize,
    DeleteSerializer,
)
from app.utils import (
    post_and_admin
)
from app.models import Company, UserForCompany


class AdminMethods:
    @staticmethod
    def get_admin_page(request):
        """get admin page"""

        users = User.objects.all().exclude(username='gena').order_by('id').filter(is_superuser=False)
        if request.user.is_superuser:
            return render(request, 'admin/admin.html', context={
                'users': users
            })
        elif not request.user.is_authenticated:
            return redirect('/')
        else:
            return redirect('/app/user-page/')

    @staticmethod
    def get_new_user_page(request):
        if request.user.is_superuser:
            return render(request, 'admin/new_user.html', context={
                'companies': Company.objects.all()
            })
        else:
            return redirect("/app/user-page/")

    @staticmethod
    def new_user(request):
        """add new user in db"""

        if not post_and_admin(request):
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        # get data from request
        try:
            data = json.loads(request.body)
        except:
            data = {}

        # work with company
        company_name_str = data.get('company', None)
        if type(company_name_str) != str:
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        if len(Company.objects.filter(name=company_name_str)) == 0:
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        company = Company.objects.filter(name=company_name_str)[0]

        # control validation for data
        if not AuthSerizliser(data=data).is_valid():
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

        user = User.objects.create_user(
            username=data.get('login'),
            password=data.get('password')
        )
        UserForCompany.objects.create(
            user=user,
            company=company
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

        # get name for user company
        user_company_name = UserForCompany.objects.get(
            user=user
        ).company.name

        # get names of all companies
        companies = []
        for i in Company.objects.all().exclude(name=user_company_name):
            companies.append(i.name)

        if request.user.is_superuser:
            return render(request, 'admin/update_user.html', context={
                "login": user.username,
                "companies": companies,
                "user_company": user_company_name
            })
        else:
            return redirect('/app/admin/')

    @staticmethod
    def update_user(request):
        if not post_and_admin(request):
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
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        # control company
        companies = Company.objects.filter(name=data.get('company'))
        if len(companies) == 0:
            return JsonResponse(data={
                "error": "4"
            }, status=400)
        else:
            # get company for working
            company = companies[0]

            # control user_and_company model
            try:
                user_for_company = UserForCompany.objects.get(user=request.user)
            except:
                return JsonResponse(data={
                    "error": "4"
                }, status=400)

            user_for_company.company = company
            user_for_company.save()

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
            return JsonResponse(data={
                "error": "1"
            }, status=400)

        if not request.user.is_superuser:
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
            return JsonResponse(data={
                "error": "3"
            }, status=400)

        # delete data from db
        for i in User.objects.filter(username=data.get('login')):
            i.delete()

        return JsonResponse(data={}, status=200)
