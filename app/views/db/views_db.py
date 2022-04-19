import pathlib
import datetime

from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import JsonResponse

# for exceptions
from django.db.utils import IntegrityError

from app.models import (
    ResultModel, RequestModel, MailForMessageModel,
    MessageModel, Company, UserForCompany
)


class DbMethods:
    """class for using db"""

    @staticmethod
    def drop_data_from_db():
        """drop data from all tables"""

        for i in MailForMessageModel.objects.all():
            i.delete()

        for i in MessageModel.objects.all():
            i.delete()

        for i in ResultModel.objects.all():
            i.delete()

        for i in RequestModel.objects.all():
            i.delete()

        for i in UserForCompany.objects.all():
            i.delete()

        for i in Company.objects.all():
            i.delete()

        for i in User.objects.all():
            i.delete()

    @staticmethod
    def control_word(word):
        """valid username(password) or no"""

        if type(word) != str:
            return True

        if word == '':
            return True

        return False

    @staticmethod
    def create_company(company_name):
        """add company object with name"""

        company_object = Company()
        company_object.name = company_name
        company_object.save()

        return company_object

    @staticmethod
    def create_admin(username, password):
        """create admin and add to db"""

        user = User.objects.create_superuser(
            username=username,
            email=username + '@gmail.com',
            password=password
        )

        return user

    @staticmethod
    def create_users():
        """create 50 users"""

        user_list = []
        for i in range(0, 50):
            try:
                # create user object
                user = User()
                user.username = str(i) + '@gmail.com'
                user.set_password('Pass@word1')
                user.save()

                # add user object to list
                user_list.append(user)
            except IntegrityError:
                pass

        return user_list

    @staticmethod
    def link_users_with_company(company, admin, user_list):
        """create link in db with users and company"""

        # work with admin
        UserForCompany.objects.create(
            user=admin,
            company=company
        )

        # work with other users
        for i in user_list:
            UserForCompany.objects.create(
                user=i,
                company=company
            )

    @staticmethod
    def add_request_data(company_object):
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
                company=company_object
            )

            if index_system % 2:
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

    @staticmethod
    def add_mails():
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

    @staticmethod
    def add_letter():
        """add latter to db"""

        # create text for adding
        file_name = str(pathlib.Path(__file__).resolve().parent)
        file_name += '/example.html'

        with open(file_name, 'r') as file:
            text_for_db = file.read()

        # get user 
        user = User.objects.get(
            username='0@gmail.com'
        )

        # add to table
        hz_index = 0
        for i in RequestModel.objects.all():
            if hz_index != 0:
                MessageModel.objects.create(
                    user=user,
                    mail='genag4448@gmail.com',
                    datetime=datetime.datetime.now(),
                    route='from',
                    message=text_for_db,
                    number='10-10',
                    request=i
                )
            hz_index += 1

        hz_index = 0
        for i in RequestModel.objects.all():
            if hz_index != 0:
                MessageModel.objects.create(
                    user=user,
                    mail='genag4448@gmail.com',
                    datetime=datetime.datetime.now(),
                    route='to',
                    message=text_for_db,
                    number='10-10',
                    request=i
                )
            hz_index += 1


class DbView:
    """view's methods for work with db"""

    @staticmethod
    def get_db_page(request):
        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })

    @staticmethod
    def delete(request):
        DbMethods.drop_data_from_db()

        return JsonResponse(data={}, status=200)

    @staticmethod
    def create(request):
        """create admin and 50 users"""

        # get data and control this
        data = {
            'login': request.POST.get('login', None),
            'password': request.POST.get('password', None)
        }
        if DbMethods.control_word(data.get('login')):
            return render(request, 'db/db.html', context={
                'login': True,
                'password': False
            })
        if DbMethods.control_word(data.get('password')):
            return render(request, 'db/db.html', context={
                'login': False,
                'password': True
            })

        # delete data from db
        DbMethods.drop_data_from_db()

        # create company, admin, users
        company_obj = DbMethods.create_company('name')
        admin_obj = DbMethods.create_admin(
            data.get('login'),
            data.get('password')
        )
        user_obj_list = DbMethods.create_users()

        # create link with users and company
        DbMethods.link_users_with_company(
            company_obj, admin_obj, user_obj_list
        )

        # create request
        DbMethods.add_request_data(company_obj)

        # DbMethods.add_mails()
        # DbMethods.add_letter()

        return render(request, 'db/db.html', context={
            'login': False,
            'password': False
        })
