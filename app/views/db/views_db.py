import datetime

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.http import JsonResponse

# for exceptions
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from app.models import (
    ResultModel, RequestModel
)


class DbMethods:
    """class for using db"""

    def drop_data_from_db(self):
        """drop data from all tables"""

        for i in ResultModel.objects.all():
            i.delete()

        for i in RequestModel.objects.all():
            i.delete()

        for i in Session.objects.all():
            i.delete()

        for i in User.objects.all():
            i.delete()

    def control_username(self, username):
        """valid username or no"""

        if type(username) != str:
            return True

        if username == '':
            return True

        return False

    def control_password(self, password):
        """valid username or no"""

        if type(password) != str:
            return True

        if password == '':
            return True

        return False
    
    def create_admin(self, username, password):
        """create admin and add to db"""

        User.objects.create_superuser(
            username=username,
            email=username + '@gmail.com',
            password=password
        )

    def create_users(self):
        """create 50 users"""

        for i in range(0, 50):
            try:
                User.objects.create_user(
                    username=str(i) + '@gmail.com',
                    password='Pass@word1'
                )
            except IntegrityError:
                pass

    def add_request_data(self):
        """add some request to db"""

        # list with data 
        data_list = [
            {
                'name': 'окна', 
                'words': 'купить окна белые пластиковые'
            },
            {
                'name': 'окна', 
                'words': 'купить окна черные пластиковые'
            },
            {
                'name': 'двери', 
                'words': 'купить двери белые'
            },
            {
                'name': 'двери', 
                'words': 'купить двери черыне'
            }
        ] 

        # add data
        for i in data_list:
            request_object = RequestModel.objects.create(
                name=i.get('name'),
                words=i.get('words'),
                datetime_created=datetime.datetime.now(),
                datetime_google_started=datetime.datetime.now(),
                datetime_google_finished=datetime.datetime.now(),
                datetime_yandex_started=datetime.datetime.now(),
                datetime_yandex_finished=datetime.datetime.now(),
                datetime_site_parsing_started=datetime.datetime.now(),
                datetime_processing_finished=datetime.datetime.now(),
                user=User.objects.all()[1]
            )

            # get google results
            for j in range(0, 10):
                ResultModel.objects.create(
                    request=request_object,
                    system='google',
                    url='https://vk.com',
                    status=True,
                    mail='genag4448@gmail.com'
                )
            

class DbView:
    @staticmethod
    def get_db_page(request):
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })

    @staticmethod
    def delete(request):
        db_object = DbMethods()
        db_object.drop_data_from_db()

        return JsonResponse(data={}, status=200)

    @staticmethod
    def create(request):
        if request.method != 'POST':
            return JsonResponse(data={
                'error': '1'
            })

        # get data and control this
        db_object = DbMethods()
        data = {
            'login': request.POST.get('login', None),
            'password': request.POST.get('password', None)
        }
        if db_object.control_username(data.get('login')):
            return render(request, 'db/db.html', context={
                'login': True,
                'password': False
            })
        if db_object.control_password(data.get('password')):
            return render(request, 'db/db.html', context={
                'login': False,
                'password': True
            })

        # delete and create data
        db_object.drop_data_from_db()
        db_object.create_admin(
            data.get('login'), 
            data.get('password')
        )
        db_object.create_users()
        db_object.add_request_data()
        
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })




