from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.http import JsonResponse

# for exceptions
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError


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
            try:
                i.delete()
            except ProtectedError:
                pass

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
            try:
                i.delete()
            except ProtectedError:
                pass

        for i in Session.objects.all():
            i.delete()

        # create superuser and add his to model
        try:
            User.objects.create_superuser(
                username=data.get('login'),
                email=data.get('login') + '@gmail.com',
                password=data.get('password')
            )
        except IntegrityError:
            pass

        for i in range(0, 50):
            try:
                User.objects.create_user(
                    username=str(i) + '@gmail.com',
                    password='Pass@word1'
                )
            except IntegrityError:
                pass
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })




