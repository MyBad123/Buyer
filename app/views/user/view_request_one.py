import json
from urllib import parse
from django.shortcuts import (
    render,
    redirect
)
from app.models import (
    RequestModel, ResultModel, MailForMessageModel,
    UserForCompany, MessageModel
)
from app.serializers import (
    RequestsSerializer,
    RequestsTableSerializer
)
from django.http import JsonResponse


class ForRequestOneView:
    def __init__(self, data):
        self.data = data
        self.message = None

    def get_items_without_duplicate(self):
        """get urls without duplicate"""

        same_urls = []
        urls_for_getting = []
        for i in self.data:
            if parse.urlparse(i.url).netloc not in same_urls:
                same_urls.append(parse.urlparse(i.url).netloc)
                urls_for_getting.append(i.url)

        return {
            'count': len(urls_for_getting),
            'urls': urls_for_getting
        }

    def set_message(self, message):
        """set all messages from chat to self.message"""

        self.message = message

    def get_message_read_no_read(self):
        """get status of reading for chats"""

        if self.message is None:
            return {
                'read': 0,
                'no_read': 0,
                'from': 0,
                'all': 0
            }

        return {
            'read': len(MessageModel.objects.filter(see='yes')),
            'no_read': len(MessageModel.objects.filter(see='no')),
            'from': len(MessageModel.objects.filter(see='from')),
            'all': len(MessageModel.objects.all())
        }


class RequestOneView:
    @staticmethod
    def no_request_redirect(request):
        return redirect('/')

    @staticmethod
    def get_site_name(mail_for_message):
        """get site for mail"""
        
        result_object = ResultModel.objects.get(
            request=mail_for_message.request,
            mail=mail_for_message.mail
        )

        return parse.urlparse(result_object.url).netloc
    
    @staticmethod
    def get_request(request, id):
        """get page with one request. get more information"""

        # control user on permissions
        if request.user.is_anonymous:
            return redirect('/')

        # get company for this request
        try:
            company = UserForCompany.objects.get(
                user=request.user
            ).company
        except UserForCompany.DoesNotExist:
            return redirect('/')

        # get object
        try:
            request_object = RequestModel.objects.get(
                id=id, company=company
            )
        except RequestModel.DoesNotExist:
            return redirect('/')

        # work with context
        context = RequestsTableSerializer.get_data_for_one(
            RequestsSerializer(request_object)
        )

        # get number of results
        for_results_obj = ForRequestOneView(
            ResultModel.objects.filter(request=request_object)
        )
        results = for_results_obj.get_items_without_duplicate().get('count')


        control_results = len(ResultModel.objects.filter(
            request=request_object,
            status=True
        ))
        if control_results > results:
            control_results = results
        
        # get data for modificate template
        results_bool = True if results else False
        all_results_bool = True if request_object.datetime_yandex_finished is None else False
        control_results_bool = True if request_object.datetime_processing_finished is None else False

        # work with data for chat
        for_messages_bool = MessageModel.objects.filter(
            mail__request=request_object,
            mail__user=request.user
        ).order_by('-datetime').order_by('mail_id').distinct('mail_id')
        messages_bool = True if len(for_messages_bool) else False
        
        messages_struct = []
        messages_struct_class = ForRequestOneView(None)
        for i in for_messages_bool:
            messages_struct_class.set_message(i.mail)
            messages_struct.append({
                'id': i.mail.id,
                'mail': i.mail.mail,
                'site_name': i.mail.site,
                'site_read': messages_struct_class.get_message_read_no_read()
            })

        # it is my request(or no)
        if request.user == request_object.creator:
            is_creator = True
        else:
            is_creator = False

        # update context with new_data
        context.update({
            'results': results,
            'control_results': control_results,
            'results_bool': results_bool,
            'all_results_bool': all_results_bool,
            'control_results_bool': control_results_bool,
            'messages_bool': messages_bool,
            'messages': messages_struct,
            'is_creator': is_creator,
            'id_for_link': id
        })

        return render(
            request,
            'user/request_one/request_one.html',
            context=context
        )

    @staticmethod
    def delete_request(request, id):
        """delete request if user is creator"""

        # control id
        try:
            request_object = RequestModel.objects.get(id=id)
        except RequestModel.DoesNotExist:
            return redirect('/')

        # control user
        if request.user == request_object.creator:
            request_object.delete_status = True
            request_object.save()

        return redirect('/')
