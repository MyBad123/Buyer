from urllib import parse
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import (
    RequestModel, ResultModel, Company
)


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


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'name'
        ]


class RequestsSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = RequestModel
        fields = [
            'id', 'words', 'name', 'datetime_created', 'datetime_google_started',
            'datetime_google_finished', 'datetime_yandex_started',
            'datetime_yandex_finished', 'datetime_site_parsing_started',
            'datetime_processing_finished', 'delete_status', 'company'
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

            if i.get('delete_status') != True:
                data.append({
                    'name': i.get('name'),
                    'date_creation': f'{ date[8:10] }.{ date[5:7] }.{ date[0:4] }',
                    'status': status,
                    'user': i.get('company').get('name'),
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
            'id': serializer.data.get('id'),
            'name': serializer.data.get('name'),
            'words': serializer.data.get('words'),
            'user': serializer.data.get('company').get('name'),
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


class ResultSerialzier(serializers.ModelSerializer):
    """serializer for ResultModel"""

    class Meta:
        model = ResultModel
        fields = '__all__'


class ForResultSerialzier:
    """utils for ResultSerialzier"""

    def __init__(self, serializer):
        self.serializer = serializer

    def get_data(self):
        """convert OrderList to list"""

        list_data = []
        for i in self.serializer.data:
            list_data.append({
                'id': i.get('id'),
                'system': i.get('system'),
                'url': i.get('url')
            })

        return list_data

    def get_control_data(self):
        """convert control OrderList to list"""

        roots_arr = []
        data_after_root = {
            
        }

        for i in self.serializer.data:
            # parce url and get to root_list
            parse_object = parse.urlparse(
                i.get('url')
            )
            if not parse_object.netloc in roots_arr:
                # add url for control in future
                roots_arr.append(parse_object.netloc)

                # add data for user
                data_after_root.update({
                    parse_object.netloc: {
                        'mail': i.get('mail'),
                        'system': i.get('system'),
                        'urls': [{
                            'url': i.get('url'),
                            'number': str(1)
                        }],
                        'contact': parse_object.netloc + '/contact/'
                    }
                })

            else:
                # get data for update
                user_object = data_after_root.get(parse_object.netloc)
                user_object_mail = user_object.get('mail')
                user_object_system = user_object.get('system')
                user_object_urls = user_object.get('urls')

                # add new url to all urls
                user_object_urls.append({
                    'url': i.get('url'),
                    'number': str(len(user_object_urls) + 1)
                })

                # update data
                data_after_root.update({
                    parse_object.netloc: {
                        'mail': user_object_mail,
                        'system': user_object_system,
                        'urls': user_object_urls,
                        'contact': parse_object.netloc + '/contact/'
                    }
                })
        
        # update data for return
        list_data = []
        for i in data_after_root.keys():
            list_data.append({
                'root': i,
                'mail': data_after_root.get(i).get('mail'),
                'system': data_after_root.get(i).get('system'),
                'urls': data_after_root.get(i).get('urls'),
                'contact': data_after_root.get(i).get('contact')
            })

        return list_data
