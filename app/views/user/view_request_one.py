from urllib import parse
from django.shortcuts import (
    render,
    redirect
)
from app.models import (
    RequestModel, ResultModel, MailForMessageModel,
    UserForCompany
)
from app.serializers import (
    RequestsSerializer,
    RequestsTableSerializer
)


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
        results = len(ResultModel.objects.filter(
            request=request_object
        ))
        control_results = len(ResultModel.objects.filter(
            request=request_object,
            status=True
        ))
        
        # get data for modificate template
        results_bool = True if results else False
        all_results_bool = True if request_object.datetime_yandex_finished is None else False
        control_results_bool = True if request_object.datetime_processing_finished is None else False

        # work with data for chat
        for_messages_bool = MailForMessageModel.objects.filter(
            request=request_object
        )
        messages_bool = True if len(for_messages_bool) else False
        
        messages = []
        messages_struct = []
        for i in for_messages_bool:
            if i.mail not in messages:
                messages.append(i.mail)
                messages_struct.append({
                    'id': i.id,
                    'mail': i.mail,
                    'site_name': RequestOneView.get_site_name(i)
                })

        # it is my request(or no)
        if request.user == request_object.creator:
            is_creator = True
        else:
            is_creator = False

        print(is_creator)
    
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
