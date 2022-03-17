import json

from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import MessageModel, MailForMessageModel
from .utils_chat import ChatUtils


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

    def message_get(request, pk):
        """get message"""

        # object for use utilities
        utils_object = ChatUtils()

        # control permission for user 
        if utils_object.control_permissions(request):
            return JsonResponse(data={
                'error': 'error of permissions'
            }, status=400)

        # control pk(id of chat)
        try:
            chat_object = MailForMessageModel.objects.get(id=pk)
        except MailForMessageModel.DoesNotExist:
            return JsonResponse(data={
                'error': 'bad data'
            }, status=400)

        # get all messages for context
        context = {
            'messages': utils_object.get_all_messages(
                request.user, chat_object.mail
            )
        }

        # get number of messages
        number = True if len(context.get('messages')) else False

        context.update({
            'number_bool': number
        })

        return JsonResponse(data=context)
