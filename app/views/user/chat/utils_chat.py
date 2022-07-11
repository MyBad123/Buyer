from datetime import datetime

from app.models import (
    MessageModel, MailForMessageModel, ParsingAttributes
)
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
        if mail_object is None:
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


class ForGetPageWithMail:
    """different utils for /chat/ request"""

    def __init__(self):
        self.chat_obj = None

    @staticmethod
    def get_correct_datetime(dt: datetime) -> str:
        """get correct str with datetime"""

        return f'{dt.hour}:{dt.minute}:{dt.second} {dt.day}.{dt.month}.{dt.year}'

    def set_chat_obj(self, id_obj) -> bool:
        """get MailForMessageModel object"""

        try:
            self.chat_obj = MailForMessageModel.objects.get(id=id_obj)
        except MailForMessageModel.DoesNotExist:
            return False

        return True

    def get_messages(self):
        """get all messages by MailForMessageModel"""

        return MessageModel.objects.filter(
            mail=self.chat_obj
        )

    def get_messages_serializer(self):
        """get all messages by MailForMessageModel with normal data"""

        struct = []
        for i in self.get_messages():
            # work with values "people"
            for_people = 0
            people = ''
            for j in ParsingAttributes.objects.filter(name='people', message=i):
                if for_people != 0:
                    people += ', '

                people += j.value
                for_people += 1

            if for_people == 0:
                people = '0 человек'

            # work with value "emails"
            for_emails = 0
            emails = ''
            for j in ParsingAttributes.objects.filter(name='emails', message=i):
                if for_emails != 0:
                    emails += ', '

                emails += j.value
                for_emails += 1

            if for_emails == 0:
                emails = '0 адресов электронной почты'

            # work with value "phones"
            for_phones = 0
            phones = ''
            for j in ParsingAttributes.objects.filter(name='phones', message=i):
                if for_phones != 0:
                    phones += ', '

                phones += j.value
                for_phones += 1

            if for_phones == 0:
                phones = '0 номеров телефонов'

            # work with value "sites"
            for_sites = 0
            sites = ''
            for j in ParsingAttributes.objects.filter(name='sites', message=i):
                if for_sites != 0:
                    sites += ', '

                sites += j.value
                for_sites += 1

            if for_sites == 0:
                sites = '0 сайтов'

            # work with value "companies"
            for_companies = 0
            companies = ''
            for j in ParsingAttributes.objects.filter(name='companies', message=i):
                if for_companies != 0:
                    companies += ', '

                companies += j.value
                for_companies += 1

            if for_companies == 0:
                companies = '0 компаний'

            # work with value "addresses"
            for_addresses = 0
            addresses = ''
            for j in ParsingAttributes.objects.filter(name='addresses', message=i):
                if for_addresses != 0:
                    addresses += ', '

                addresses += j.value
                for_addresses += 1

            if for_addresses == 0:
                addresses = '0 адресов'

            # work with value "positions"
            for_positions = 0
            positions = ''
            for j in ParsingAttributes.objects.filter(name='positions', message=i):
                if for_positions != 0:
                    positions += ', '

                positions += j.value
                for_positions += 1

            if for_positions == 0:
                positions = '0 позиций'

            # get mails
            if i.route == 'from':
                for_route = False
                route = 'исходящее'
            elif i.route == 'to':
                for_route = True
                route = 'входящее'
            else:
                for_route = False
                route = 'неизвестно'

            struct.append({
                'people': people,
                'emails': emails,
                'phones': phones,
                'sites': sites,
                'companies': companies,
                'addresses': addresses,
                'positions': positions,
                'id': self.chat_obj.id,
                'id_message': i.id,
                'datetime': ForGetPageWithMail.get_correct_datetime(i.datetime),
                'route': route,
                'for_route': for_route
            })

        return struct
