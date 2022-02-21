from rest_framework import serializers
from django.contrib.auth.models import User

from .models import RequestModel

class AuthSerizliser(serializers.Serializer):
    """serializer"""

    login = serializers.CharField()
    password = serializers.CharField()


class UpdateSerialize(serializers.Serializer):

    old_name = serializers.CharField()
    new_name = serializers.CharField()
    password = serializers.CharField()


class DeleteSerializer(serializers.Serializer):

    login = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RequestsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RequestModel
        fields = [
            'id', 'words', 'name', 'datetime_created', 'datetime_google_started',
            'datetime_google_finished', 'datetime_yandex_started',
            'datetime_yandex_finished', 'datetime_site_parsing_started',
            'datetime_processing_finished', 'user'
        ]


class RequestsTableSerializer(serializers.ModelSerializer):
    """get data for user's table"""

    @staticmethod
    def get_data(serializer):
        data = []
        for i in serializer.data:
            # get date
            date = i.get('datetime_created')

            # get status
            if i.get('datetime_google_started') == None:
                status = 'в очереди'
            elif i.get('datetime_google_finished') == None:
                status = 'поиск в google search начался'
            elif i.get('datetime_yandex_started') == None:
                status = 'поиск в google search закончился'
            elif i.get('datetime_yandex_finished') == None:
                status = 'поиск в yandex search начался'
            elif i.get('datetime_site_parsing_started') == None:
                status = 'поиск в yandex search закончился'
            elif i.get('datetime_processing_finished') == None:
                status = 'ссылки в обработке'
            else:
                status = 'окончание'

            data.append({
                'name': i.get('name'),
                'date_creation': f'{ date[8:10] }.{ date[5:7] }.{ date[0:4] }',
                'status': status,
                'user': i.get('user').get('username'),
                'id': i.get('id')
            })

        return data

    @staticmethod
    def get_data_for_one(serializer):
        """get info from one request's serializer"""

        # get stage
        if serializer.data.get('datetime_google_started') == None:
            stage = 'в очереди'
        elif serializer.data.get('datetime_google_finished') == None:
            stage = 'поиск в google search начался'
        elif serializer.data.get('datetime_yandex_started') == None:
            stage = 'поиск в google search закончился'
        elif serializer.data.get('datetime_yandex_finished') == None:
            stage = 'поиск в yandex search начался'
        elif serializer.data.get('datetime_site_parsing_started') == None:
            stage = 'поиск в yandex search закончился'
        elif serializer.data.get('datetime_processing_finished') == None:
            stage = 'ссылки в обработке'
        else:
            stage = 'окончание'

        # get datetime for start
        dt = serializer.data.get('datetime_created')
        datetime_created = f'{ dt[8:10] }.{ dt[5:7] }.{ dt[0:4] }'
        datetime_created += f' '
        datetime_created += f'{ dt[11:13] }:{ dt[14:16] }:{ dt[17:19] }'

        #
        if serializer.data.get('datetime_google_started') != None:
            datetime_google_started_bool = True
            dt = serializer.data.get('datetime_google_started')
            datetime_google_started = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_google_started += f' '
            datetime_google_started += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_google_started_bool = False
            datetime_google_started = None

        if serializer.data.get('datetime_google_finished') != None:
            datetime_google_finished_bool = True
            dt = serializer.data.get('datetime_google_finished')
            datetime_google_finished = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_google_finished += f' '
            datetime_google_finished += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_google_finished_bool = False
            datetime_google_finished = None

        if serializer.data.get('datetime_yandex_started') != None:
            datetime_yandex_started_bool = True
            dt = serializer.data.get('datetime_yandex_started')
            datetime_yandex_started = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_yandex_started += f' '
            datetime_yandex_started += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_yandex_started_bool = False
            datetime_yandex_started = None

        if serializer.data.get('datetime_yandex_finished') != None:
            datetime_yandex_finished_bool = True
            dt = serializer.data.get('datetime_yandex_finished')
            datetime_yandex_finished = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_yandex_finished += f' '
            datetime_yandex_finished += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_yandex_finished_bool = False
            datetime_yandex_finished = None

        if serializer.data.get('datetime_site_parsing_started') != None:
            datetime_site_parsing_started_bool = True
            dt = serializer.data.get('datetime_site_parsing_started')
            datetime_site_parsing_started = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_site_parsing_started += f' '
            datetime_site_parsing_started += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_site_parsing_started_bool = False
            datetime_site_parsing_started = None

        if serializer.data.get('datetime_processing_finished') != None:
            datetime_processing_finished_bool = True
            dt = serializer.data.get('datetime_processing_finished')
            datetime_processing_finished = f'{dt[8:10]}.{dt[5:7]}.{dt[0:4]}'
            datetime_processing_finished += f' '
            datetime_processing_finished += f'{dt[11:13]}:{dt[14:16]}:{dt[17:19]}'
        else:
            datetime_processing_finished_bool = False
            datetime_processing_finished = None



        return {
            'name': serializer.data.get('name'),
            'words': serializer.data.get('words'),
            'user': serializer.data.get('user').get('username'),
            'stage': stage,
            'datetime_created': datetime_created,

            'datetime_google_started_bool': datetime_google_started_bool,
            'datetime_google_started': datetime_google_started,
            'datetime_google_finished_bool': datetime_google_finished_bool,
            'datetime_google_finished': datetime_google_finished,
            'datetime_yandex_started_bool': datetime_yandex_started_bool,
            'datetime_yandex_started': datetime_yandex_started,
            'datetime_yandex_finished_bool': datetime_yandex_finished_bool,
            'datetime_yandex_finished': datetime_yandex_finished,
            'datetime_site_parsing_started_bool': datetime_site_parsing_started_bool,
            'datetime_site_parsing_started': datetime_site_parsing_started,
            'datetime_processing_finished_bool': datetime_processing_finished_bool,
            'datetime_processing_finished': datetime_processing_finished
        }