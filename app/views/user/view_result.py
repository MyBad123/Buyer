import json 

from email.utils import parseaddr
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import RequestModel, ResultModel
from app.serializers import ResultSerialzier, ForResultSerialzier

from request.tasks import send

class MessageControlDataError(Exception):
    pass


class MessageControlData:
    """control data of message"""

    def __init__(self, data):
        self.data = data

    def control_data_type(self):
        """data is dict or no"""

        if type(self.data) != dict:
            return True

        return False

    def control_id_request(self):
        """control request_id"""

        # work with types
        try:
            request_id = int(self.data.get('request_id'))
        except ValueError:
            return True

        # work with model
        try: 
            RequestModel.objects.get(id=request_id)
        except RequestModel.DoesNotExist:
            return True

        return False        

    def control_type_fields(self):
        """control mails and text"""

        # control availability of fields
        if self.data.get('text', None) is None:
            return True

        if self.data.get('mails', None) is None:
            return True 

        if self.data.get('request_id', None) is None:
            return True 

        # control type of data fields
        if type(self.data.get('text')) != str:
            return True

        if type(self.data.get('mails')) != list:
            return True

        for i in self.data.get('mails'):
            if type(i) != str:
                return True

        if type(self.data.get('request_id')) != str:
            return True

        return False

    def all_control(self):
        """use all methods in this class"""

        if self.control_data_type():
            return True

        if self.control_type_fields():
            return True

        if self.control_id_request():
            return True

        return False


class MessageUtils(MessageControlData):
    """metods for send_messages in view"""

    def __init__(self, request):
        
        # control data
        if self.control_permission_and_post(request):
            raise MessageControlDataError()

        # decode data
        try:
            decode_data = json.loads(request.body)
        except json.JSONDecodeError:
            raise MessageControlDataError()

        # get data for serializer
        data = {
            'text': decode_data.get('text'),
            'mails': decode_data.get('mails'), 
            'request_id': decode_data.get('request')
        }
        
        super().__init__(data)

    def control_permission_and_post(self, request):
        """method for control request and user's permission"""

        # control post or no 
        if request.method != 'POST':
            return True

        # control permission user
        if request.user.is_anonymous:
            return True

        return False

    def send_message(self, user):
        """send message to all mails"""

        # update data
        self.data.update({
            'user': user.id
        })

        print(self.data)

        send.delay(self.data)
        

class ResultsView:
    """views for result"""

    @staticmethod
    def control_user_and_id(request, pk):
        """control permissions """

        # control user
        if request.user.is_anonymous:
            return True

        # control id
        try:
            RequestModel.objects.get(id=pk)
        except RequestModel.DoesNotExist:
            return True

        return False

    @staticmethod
    def get_result_page(request, pk):
        """get all results of request"""
        
        # control permissions and pk
        if ResultsView.control_user_and_id(request, pk):
            return redirect('/')
        else:
            request_object = RequestModel.objects.get(id=pk)

        # work with context 
        context = {
            'name': request_object.name,
            'words': request_object.words,
            'id': pk
        }

        # get all results(with serializer) and update context
        results = ResultModel.objects.filter(request=request_object)
        results_serializer = ForResultSerialzier(
            serializer=ResultSerialzier(results, many=True)
        )
        context.update({
            'results_serializer': results_serializer.get_data()
        })

        # get pk to context for work with refs
        context.update({
            'pk': pk
        })

        return render(
            request, 
            'user/request_one/all_results.html',
            context=context
        )

    @staticmethod
    def get_correct_result_page(request, pk):
        """get results for push mail"""

        # control permissions and pk
        if ResultsView.control_user_and_id(request, pk):
            return redirect('/')
        else:
            request_object = RequestModel.objects.get(id=pk)

        # get objects and add data of this on context
        result_objects = ResultModel.objects.filter(
            request=request_object,
            status=True
        )
        context = {
            'name': request_object.name,
            'words': request_object.words,
            'id': pk
        }
        serializer = ForResultSerialzier(ResultSerialzier(
            result_objects, 
            many=True
        ))
        context.update({
            'results_serializer': serializer.get_control_data()
        })

        # get pk to context for work with refs
        context.update({
            'pk': pk
        })

        return render(
            request, 
            'user/request_one/all_control_results.html',
            context=context
        )

    @staticmethod
    def send_messages(request):
        """method for send to mail"""
        
        # to initialize control object for this func
        try:
            utils_object = MessageUtils(request)
        except MessageControlDataError:
            return JsonResponse(data={
                'error': 'this user does not have access'
            }, status=400)
        
        # control data in serializer
        if utils_object.all_control():
            return JsonResponse(data={
                'erorr': 'bad data'
            }, status=400)

        # send message
        utils_object.send_message(request.user)

        return JsonResponse(data={})

    @staticmethod
    def thanks_after_message(request, pk):
        """thank the user for sending a message"""

        # control permissions and pk
        if ResultsView.control_user_and_id(request, pk):
            return redirect('/')

        return render(request, 'user/request_one/thanks.html', context={
            'pk': pk
        })