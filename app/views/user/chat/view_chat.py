import json
import datetime

from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import (
    MailForMessageModel, MessageModel, ParsingAttributes
)
from .utils_chat import (
    ChatUtils, GetMailsUtils, ForGetPageWithMail
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
            'id_mail': mail_obj.id,
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
        for_get_mails = ForGetPageWithMail()
        for_get_mails.set_chat_obj(pk)

        return render(
            request,
            'user/chat/chat_with.html',
            context={
                'id_request': mail.request.id,
                'id_chat': mail.id,
                'mails': for_get_mails.get_messages_serializer(),
                'request_word': mail.request.name,
                'request_vendor': mail.site
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
            'id_request': mail_for_obj.request.id,
            'id_mail_for_message_model': pk,
            'mail': mail_for_obj.mail
        })

    @staticmethod
    def get_page_after_parsing(request, pk):
        """get some info after parsing mail_hendler"""

        # control id(pk)
        try:
            mail_obj = MessageModel.objects.get(id=pk)
        except MessageModel.DoesNotExist:
            return redirect(f'/chat/{ str(pk) }/')

        # control permission
        if mail_obj.mail.user != request.user:
            return redirect(f'/chat/{ str(pk) }/')

        # control parameter from user
        params_arr = [
            'people', 'emails', 'phones', 'sites',
            'companies', 'addresses', 'positions',
            'text'
        ]
        user_param = request.GET.get('parameter', None)

        if not user_param in params_arr:
            return redirect(f'/chat/{str(pk)}/')

        # send data to contex for work with template
        is_text = True if user_param == 'text' else False

        if is_text:
            content = mail_obj.message
        else:
            for_content = ParsingAttributes.objects.filter(
                name=user_param,
                message=mail_obj
            )

            for_index = 0
            content = ''

            for i in for_content:
                if for_index != 0:
                    content += ', '

                content += i.value
                for_index += 1

        return render(request, 'user/chat/chat_after_parsing.html', context={
            'id_request': mail_obj.mail.request.id,
            'id_chat': mail_obj.mail.id,
            'is_text': is_text,
            'content': content,
            'type': user_param
        })
