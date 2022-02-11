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
        fields = ['name', 'datetime_on_search', 'datetime_on_tree', 'user']


class RequestsTableSerializer(serializers.ModelSerializer):
    """get data for user's table"""

    @staticmethod
    def get_data(serializer):
        data = []
        for i in serializer.data:
            # get date
            date = i.get('datetime_on_search')

            # get status
            if i.get('datetime_on_tree') is None:
                status = 'on search'
            else:
                status = 'on analise'
            data.append({
                'name': i.get('name'),
                'date_creation': f'{ date[8:10] }.{ date[5:7] }.{ date[0:4] }',
                'status': i.get('status'),
                'user': i.get('user').get('username')
            })

        return data
