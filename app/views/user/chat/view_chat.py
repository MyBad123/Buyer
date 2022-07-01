import json
import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import MessageModel, MailForMessageModel
from .utils_chat import (
    ChatUtils, GetMailsUtils, SendMessageUtils
)
from request.tasks import send


class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        return redirect('/')

    @staticmethod
    def send_thank(request, pk):
        """get page after sending message on mail"""

        try:
            mail_obj = MailForMessageModel.objects.get(id=pk)
        except MailForMessageModel.DoesNotExist:
            return redirect('/')

        return render(request, 'user/chat/chat_thanks.html', context={
            'id_request': mail_obj.request.id,
            'mails': mail_obj.mail
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
        mail = utils_object.control_mail_from_request(pk)
        if mail is None:
            return redirect('/chat/')

        # control permission
        if mail.user != request.user:
            return redirect('/chat/')

        # get data for table in /chat/<pk:int>/
        get_mails_obj = GetMailsUtils()
        get_mails = get_mails_obj.get_all_messages(
            mail.user,
            mail.mail,
            mail.request,
            mail.id
        )

        return render(
            request, 
            'user/chat/chat_with.html',
            context={
                'id_request': mail.request.id,
                'mails': get_mails
            }
        )

    @staticmethod
    def send_message(request, pk):
        """send message to mail"""

        if request.method == 'POST':
            # control pk
            try:
                mail_for_obj = MailForMessageModel.objects.get(id=pk)
            except MailForMessageModel.DoesNotExist:
                return redirect(f'/chat/{ str(pk) }/')

            # control permission
            if mail_for_obj.user != request.user:
                return redirect(f'/chat/{str(pk)}/')

            # control message
            if request.POST.get('text', None) is None:
                return redirect(f'/chat/{str(pk)}/')

            if type(request.POST.get('text', None)) != str:
                return redirect(f'/chat/{str(pk)}/')

            if request.POST.get('text', None) == '':
                return redirect(f'/chat/{str(pk)}/')

            # save message and send
            send.delay({
                'text': request.POST.get('text', None),
                'mails': [{
                    'mail': mail_for_obj.mail,
                    'site': mail_for_obj.site
                }],
                'request_id': mail_for_obj.request.id,
                'user': request.user.id,
                'chats': [mail_for_obj.id]
            })

            return redirect(f'/chat-thanks/{ str(pk) }/')
        else:
            return redirect(f'/chat/{ str(pk) }/')

    @staticmethod
    def get_page_send_mesage(request, pk):
        # get MailForMessageModel
        try:
            mail_for_obj = MailForMessageModel.objects.get(id=pk)
        except MailForMessageModel.DoesNotExist:
            return redirect(
                '/chat/' + str(pk) + '/'
            )

        # control permission
        if mail_for_obj.user != request.user:
            return redirect(
                '/chat/' + str(pk) + '/'
            )

        return render(request, 'user/chat/chat_send.html', context={
            'id_mail_for_message_model': pk,
            'mail': mail_for_obj.mail
        })
