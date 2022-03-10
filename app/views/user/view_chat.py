from email import message
from tkinter import E
from django.shortcuts import render, redirect

from app.models import MessageModel, MailForMessageModel

class ChatUtils:
    """utility methods for ChatViews class"""

    def control_permissions(self, request):
        """control user on permissions"""

        if request.user.is_anonymous:
            return True

        return False

    def control_mail_from_request(self, request, pk):
        """get mail or no"""

        # get user
        user = request.user 

        # get mail from db 
        try:
            mail = MailForMessageModel.objects.get(id=pk).mail
        except MailForMessageModel.DoesNotExist:
            return None

        # does the user have a chat with this mail
        if len(MessageModel.objects.filter(user=user, mail=mail)) == 0:
            return None

        return mail

    def context_get_page(self, request):
        """get data for get_page func"""

        # get user 
        user = request.user

        # user have message or no
        if len(MessageModel.objects.filter(user=user)):
            bool_mail = True
        else:
            bool_mail = False

        # get all mail 
        all_mail = []
        for i in MessageModel.objects.filter(user=user).order_by('mail').distinct('mail'):
            try:
                all_mail.append({
                    'id': MailForMessageModel.objects.get(mail=i.mail).id,
                    'mail': i.mail
                })
            except MailForMessageModel.DoesNotExist:
                pass

        return {
            'bool_mail': bool_mail,
            'mail_arr': all_mail
        }

    def context_get_page_with_mail(self, user, mail):
        """get messages for user"""

        # get all messages
        messages = MessageModel.objects.filter(
            user=user, mail=mail
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


class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        # object for use utilities
        utils_object = ChatUtils()

        # control users permission 
        if utils_object.control_permissions(request):
            return redirect('/')

        return render(
            request, 
            'user/chat/chat.html',
            context=utils_object.context_get_page(request)
        )

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

        return render(
            request, 
            'user/chat/chat_with.html',
            context=context
        )

        