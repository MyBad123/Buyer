import json

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.http import JsonResponse

from app.serializers import (
    AuthSerizliser
)


class DbMethods:
    @staticmethod
    def get_db_page(request):
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })

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
        data = {
            'login': request.POST.get('login', None),
            'password': request.POST.get('password', None)
        }

        if data.get('login') is None or data.get('login') == '':
            return render(request, 'db/db.html', context={
                'login': True,
                'password': False
            })

        if data.get('password') is None or data.get('password') == '':
            return render(request, 'db/db.html', context={
                'login': False,
                'password': True
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

        for i in range(0, 50):
            User.objects.create_user(
                username=str(i) + '@gmail.com',
                password='Pass@word1'
            )
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })
