import json 

from email.utils import parseaddr
from django.http import JsonResponse
from django.shortcuts import render, redirect

from app.models import (
    RequestModel, ResultModel,
    MailForMessageModel, UserForCompany
)
from app.serializers import ResultSerialzier, ForResultSerialzier

from request.tasks import send


class MessageControlDataError(Exception):
    pass


class MessageControlData:
    """control data of message"""

    def __init__(self, data):
        self.data = data
        self.request_model = None

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
            self.request_model = RequestModel.objects.get(id=request_id)
        except RequestModel.DoesNotExist:
            return True

        return False

    def control_mail_site(self):
        """control mail and site in requests"""

        for i in self.data.get('mails'):
            query = ResultModel.objects.filter(
                request=self.request_model,
                mail=i.get('mail'),
                url__contains=i.get('site')
            )
            if len(query) == 0:
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
            # control mail
            if type(i.get('mail')) is not str or (i.get('mail') == ''):
                return True

            # control site for this mail
            if type(i.get('site')) is not str or (i.get('site') == ''):
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

    def send_message(self, user, chats_id):
        """send message to all mails"""

        # update data
        self.data.update({
            'user': user.id,
            'chats': chats_id
        })
        
        send.delay(self.data)


class ForChangeMailUtils:
    """class for work with ResultsView.change_mail"""

    def __init__(self, data):
        self.data = data

    def control_data(self) -> bool:
        """control valid self.data or no"""

        # control id
        if self.data.get('id_request') is None:
            return False

        if type(self.data.get('id_request')) != int:
            return False

        # control site
        if self.data.get('site') is None:
            return False

        if type(self.data.get('site')) != str:
            return False

        # control mail str
        if self.data.get('mail') is None:
            return False

        if type(self.data.get('mail')) != str:
            return False

        return True

    def control_permission_request(self, user):
        """control permission user to this request(RequestModel)"""

        # get object for control
        try:
            request_obj = RequestModel.objects.get(
                id=self.data.get('id_request')
            )
        except RequestModel.DoesNotExist:
            return False

        # get company for user
        companies = UserForCompany.objects.filter(
            user=user
        )
        if len(companies) == 0:
            return False

        # control permission
        for_control = 0
        for i in companies:
            if i.company.id == request_obj.company.id:
                for_control

        if for_control == 0:
            return False

        return True


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

        # add mail and site to db
        chats_id = []
        for i in utils_object.data.get('mails'):
            try:
                mail_for_message_obj = MailForMessageModel.objects.get(
                    mail=i.get('mail'),
                    request=utils_object.request_model,
                    user=request.user,
                    site=i.get('site')
                )
                chats_id.append(mail_for_message_obj.id)
            except MailForMessageModel.DoesNotExist:
                mail_for_message_obj = MailForMessageModel.objects.create(
                    mail=i.get('mail'),
                    request=utils_object.request_model,
                    user=request.user,
                    site=i.get('site')
                )
                chats_id.append(mail_for_message_obj.id)

        # send message
        utils_object.send_message(request.user, chats_id)

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

    @staticmethod
    def change_mail(request):
        """change mail"""

        # get data from request
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse(data={
                'error': 1,
                'comment': 'bad struct for data'
            }, status=400)

        # control data: valid or no
        utils_obj = ForChangeMailUtils(data=data)
        if not utils_obj.control_data():
            return JsonResponse(data={
                'error': 2,
                'comment': 'no valid data'
            }, status=400)

        # get RequestModel object
        try:
            request_obj = RequestModel.objects.get(id=data.get('id_request'))
        except RequestModel.DoesNotExist:
            return JsonResponse(data={
                'error': 3,
                'comment': 'object for request(Model) is exist'
            }, status=400)

        # control user's permission
        if not utils_obj.control_permission_request(request.user):
            return JsonResponse(data={
                'error': 4,
                'comment': 'you dont has permission for request(Model)'
            }, status=400)

        # work with changing
        results = ResultModel.objects.filter(
            request=request_obj,
            url__contains=data.get('site')
        )
        for i in results:
            i.mail = data.get('mail')
            i.save()

        return JsonResponse(data={}, status=200)
