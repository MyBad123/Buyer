import json

from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import MessageModel, MailForMessageModel
from .utils_chat import (
    ChatUtils, GetMailsUtils, SendMessageUtils
)


class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        return redirect('/')

    @staticmethod
    def get_page_with_mail(request, pk):
        """get chat with one mail"""

        # object for use utilities
        utils_object = ChatUtils()

        # control users permission
        if utils_object.control_permissions(request):
            return redirect('/')

        # control chat
        mail = utils_object.control_mail_from_request(pk)
        if mail is None:
            return redirect('/chat/')

        return render(
            request, 
            'user/chat/chat_with.html'
        )

    def message_get(request, pk):
        """get message"""

        # object for use utilities
        utils_object = GetMailsUtils()

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

    @staticmethod
    def send_message(request):
        """send message to mail"""

        # object for use utilities
        utils_object = SendMessageUtils()

        # control data

        """
        {'text': 'не хочу пиво', 'mails': ['genag4448@gmail.com'], 'request_id': '1', 'user': 2}
        """
        return JsonResponse(data={})
