from tkinter import E
from django.shortcuts import render, redirect

from app.models import MessageModel

class ChatViews:
    """methods for chat"""

    @staticmethod
    def control_permissions(request):
        """control user on permissions"""

        if request.user.is_anonymous:
            return True

        return False

    @staticmethod
    def context_get_page(request):
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
            all_mail.append(i.mail)

        return {
            'bool_mail': bool_mail,
            'mail_arr': all_mail
        }

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        # control users permission 
        if ChatViews.control_permissions(request):
            return redirect('/')

        return render(
            request, 
            'user/chat/chat.html',
            context=ChatViews.context_get_page(request)
        )
        