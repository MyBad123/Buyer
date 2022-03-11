import json
import smtplib
import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.shortcuts import render, redirect
from django.http.response import JsonResponse

from app.models import MessageModel, MailForMessageModel

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

    def send_message(self, mail, text):
        """send message to mail"""

        mailMsg = MIMEMultipart()
        mailTo = mail
        mailMessage = text
        mailMsg.attach(MIMEText(mailMessage, 'plain'))
        mailServer = smtplib.SMTP('smtp.mail.ru: 25')
        mailServer.starttls()
        mailServer.login('gena.kuznetsov@internet.ru', 'o%pdUaeIUI12')
        mailServer.sendmail('gena.kuznetsov@internet.ru', mailTo, mailMsg.as_string())
        mailServer.quit()


class PushMessage:
    """invalid data or no"""

    def __init__(self, data):
        self.data = data 

    def control_dict(self):
        """data is dict or no"""

        if type(self.data) != dict:
            return True

        return False

    def control_data_on_dict(self):
        """control names of fields"""

        # control fields 
        if self.data.get('id', None) is None:
            return True

        if self.data.get('text', None) is None:
            return True

        # control data in fields
        if type(self.data.get('id')) != str:
            return True

        if type(self.data.get('text')) != str:
            return True

        return False

    def control_id_int(self):
        """send an error if not decoded to a number"""

        try:
            int(self.data.get('id'))
        except ValueError:
            return True

        return False

    def control_data(self):
        """use all methods"""

        if self.control_dict():
            return True

        if self.control_data_on_dict():
            return True

        if self.control_id_int():
            return True

        return False


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

    @staticmethod
    def push_message(request):
        """add new message"""

        # object for use utilities
        utils_object = ChatUtils()

        # control permissions and view of request
        if utils_object.control_permissions_with_post(request):
            return JsonResponse(
                data={'message': 'c'}, 
                status=400
            )

        # control data
        try:
            data = json.loads(request.body)
        except json.decoder.JSONDecodeError:
            return JsonResponse(
                data={'message': 'invalid data'}, 
                status=400
            )

        serializer = PushMessage(data)
        if serializer.control_data():
            return JsonResponse(
                data={'message': 'invalid data'}, 
                status=400
            )

        # control permissions to mail 
        mail = utils_object.control_mail_from_request(
            request, data.get('id')
        )
        if mail is None:
            return JsonResponse(
                data={'message': 'access error'}, 
                status=400
            )

        # save to db
        message_object = MessageModel.objects.create(
            user=request.user,
            mail=mail,
            datetime=datetime.datetime.now(),
            route='from',
            message=data.get('text'),
            number=None
        )

        # update db object 
        message_object.number = str(request.user.id) + '-' + str(message_object.id)
        message_object.save()

        # send message to mail
        utils_object.send_message(
            mail=message_object.mail,
            text=message_object.message
        )

        return JsonResponse(data={})
        
