import json
import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import MessageModel, MailForMessageModel
from request.tasks import send

class ChatUtils:
    """utility methods for ChatViews class"""

    def control_permissions(self, request):
        """control user on permissions"""

        if request.user.is_anonymous:
            return True

        return False

    def control_permissions_with_post(self, request):
        """control user on permissions"""

        if request.user.is_anonymous:
            return True

        if request.method != 'POST':
            return True

        return False

    def control_mail_from_request(self, request, pk):
        """get mail or no"""

        # get mail from db 
        try:
            mail = MailForMessageModel.objects.get(id=pk)
        except MailForMessageModel.DoesNotExist:
            return None

        return mail

    def context_get_page_with_mail(self, user, mail):
        """get messages for user"""

        # get all messages
        messages = MessageModel.objects.filter(
            user=user, mail=mail.mail, 
            request=mail.request 
        )
        
        # make data for context
        data = []
        for i in messages:
            if i.route == 'from':
                route_bool = True
            else:
                route_bool = False

            data.append({
                'body': i.message,
                'route_bool': route_bool
            })

        return {
            'mail_arr': data
        }

    def get_mail_for_message_model(self, data_dict: dict):
        """control id of MailForMessageModel"""

        # control type of data_dict
        if type(data_dict) != dict:
            return None

        # control id of MailForMessageModel
        model_id = data_dict.get('id', None)
        if type(model_id) != str:
            return None

        # control type of data
        try:
            model_id = int(model_id)
        except ValueError:
            return None

        # get object from MailForMessageModel
        try:
            mail_object = MailForMessageModel.objects.get(id=model_id)
        except MailForMessageModel.DoesNotExist:
            return None

        return mail_object


class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        return redirect('/')

    @staticmethod
    def get_mail_struct(request):
        """get mail and request_id for sending mail"""

        # get utils class 
        utils_object = ChatUtils()
        
        # control permission and view of request
        if utils_object.control_permissions_with_post(request):
            return JsonResponse(data={
                'error': 'error of permissions'
            }, status=400)

        # get data from request
        try:
            data_from_request = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(data={
                'error': 'bad data'
            }, status=400)

        # get mail_object 
        mail_object = utils_object.get_mail_for_message_model(data_from_request)
        if mail_object == None:
            return JsonResponse(data={
                'error': 'bad data'
            }, status=400)

        return JsonResponse(data={
            'mail': mail_object.mail,
            'request_id': mail_object.request.id
        })
        
    @staticmethod
    def get_page_with_mail(request, pk):
        """get chat with one mail"""

        # object for use utilities
        utils_object = ChatUtils()

        # control users permission
        if utils_object.control_permissions(request):
            return redirect('/')

        # control chat
        mail = utils_object.control_mail_from_request(request, pk)
        if mail is None:
            return redirect('/chat/')

        # get all messages
        context = utils_object.context_get_page_with_mail(
            user=request.user,
            mail=mail
        )
        
        # see chat or no 
        see_chat = True if len(context.get('mail_arr')) else False
        context.update({
            'see_chat': see_chat
        })

        return render(
            request, 
            'user/chat/chat_with.html',
            context=context
        )
