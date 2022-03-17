import pathlib
import datetime

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.http import JsonResponse

# for exceptions
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError

from app.models import (
    ResultModel, RequestModel, MailForMessageModel,
    MessageModel
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
                'name': 'шашки', 
                'words': 'купить шашки такси желтые',
                'page': 'https://taxibox.ru/models/reklamniy-svetovoi-korob-na-taksi-big-1000.html'
            },
            {
                'name': 'питон', 
                'words': 'купить питон', 
                'page': 'https://exomenu.ru/python10/'
            },
            {
                'name': 'спрей', 
                'words': 'спрей для волос недорогой',  
                'page': 'https://www.tangleteezer.ru/all-brushes/hairspray/detangling-sprays/detangling-spray-for-kids/'
            },
            {
                'name': 'шапку', 
                'words': 'купить шапку женскую',
                'page': 'https://nskshapki.ru/catalog/product/id/3851/'
            },
            {
                'name': 'кроссы', 
                'words': 'четкие кроссы',
                'page': 'https://belobuv.ru/wl-1e-inblu-krossovki-zhenskie.html'
            }
        ] 

        # add data
        index_system = 0
        for i in data_list:
            index_system += 1

            user = User.objects.all()[1]
            print(user)

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
                user=user
            )
            
            if (index_system % 2):
                ResultModel.objects.create(
                    request=request_object,
                    system='google',
                    url=i.get('page'),
                    status=True,
                    mail='genag4448@gmail.com'
                )
            else:
                ResultModel.objects.create(
                    request=request_object,
                    system='yandex',
                    url=i.get('page'),
                    status=True,
                    mail='genag4448@gmail.com'
                )

    def add_mails(self):
        """add mails to result for chat"""

        # get all result objects 
        all_results = ResultModel.objects.all()

        # set mails for chat
        for i in all_results:
            try:
                MailForMessageModel.objects.get(
                    mail=i.mail,
                    request=i.request
                )
            except MailForMessageModel.DoesNotExist:
                MailForMessageModel.objects.create(
                    mail=i.mail,
                    request=i.request
                )

    def add_letter(self):
        """add latter to db"""

        # create text for adding
        file_name = str(pathlib.Path(__file__).resolve().parent)
        file_name += '/example.html'

        with open(file_name, 'r') as file:
            text_for_db = file.read()
			
        # add to table
        for i in RequestModel.objects.all():
            MessageModel.objects.create(
                user=i.user,
                mail='genag4448@gmail.com',
                datetime=datetime.datetime.now(),
                route='from',
                message=text_for_db,
                number='10-10',
                request=i
            )

        for i in RequestModel.objects.all():
            MessageModel.objects.create(
                user=i.user,
                mail='genag4448@gmail.com',
                datetime=datetime.datetime.now(),
                route='to',
                message=text_for_db,
                number='10-10',
                request=i
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
        db_object.add_mails()
        db_object.add_letter()
        
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })




