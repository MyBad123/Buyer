from datetime import datetime

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

    def control_mail_from_request(self, pk):
        """get mail or no"""

        # get mail from db 
        try:
            mail = MailForMessageModel.objects.get(id=pk)
        except MailForMessageModel.DoesNotExist:
            return None

        return mail


class GetMailsUtils(ChatUtils):
    """def utils for sending message"""
    
    def datetime_as_str(self, dt: datetime):
        """convert datetime to str"""

        return f'{dt.hour}:{dt.minute}:{dt.second} {dt.day}.{dt.month}.{dt.year}'

    def get_all_messages(self, user, mail, request, id_for_control):
        """get all messages for user by mail"""

        # get all objects
        all_messages = MessageModel.objects.filter(
            mail__user=user,
            mail__mail=mail,
            mail__request=request,
            mail__id=id_for_control
        )

        # work with data
        data = []
        for i in all_messages:
            # get route
            route_to_bool = True if i.route == 'to' else False
            
            data.append({
                'route_to_bool': route_to_bool,
                'body': i.message,
                'datetime': self.datetime_as_str(i.datetime)
            })

        return data


class SendMessageUtils(ChatUtils):
    """utils for sending message"""

    def __init__(self, data) -> None:
        self.data: dict = data
        self.mail_object = None
        super().__init__(self)

    def is_valid(self) -> bool:
        """control data"""

        # control type 
        if type(self.data) != dict:
            return True

        # control id of this chat with mail 
        if type(self.data.get('chat_id')) != str:
            return True

        try:
            chat_id = int(self.data.get('chat_id'))
        except ValueError:
            return False

        mail_object = super().control_mail_from_request(chat_id)
        if mail_object == None:
            return False
        else:
            self.mail_object = mail_object

        # control text
        if type(self.data.get('text')) != str:
            return True

        return False

    def send_message(self, request):
        """send message to mail"""

        # to organize data structure
        data_struct = {
            'text': self.data.get('text'),
            'mails': [self.mail_object.mail],
            'request_id': str(self.mail_object.request.id),
            'user': request.user.id
        }

        send.delay(data_struct)

        