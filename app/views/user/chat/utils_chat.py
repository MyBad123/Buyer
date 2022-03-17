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

    def get_all_messages(self, user, mail):
        """get all messages for user by mail"""

        # get all objects 
        all_messages = MessageModel.objects.filter(
            user=user,
            mail=mail
        )

        # work with data
        data = []
        for i in all_messages:
            # get route
            route_to_bool = True if i.route == 'to' else False
            
            data.append({
                'route_to_bool': route_to_bool,
                'body': i.message,
                'datetime': i.datetime
            })

        return data

