from unittest import result
from django.shortcuts import (
    render,
    redirect
)
from app.models import (
    RequestModel, ResultModel, MailForMessageModel
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
    def get_request(request, id):
        """get page with one request. get more information"""

        # control user on permissions
        if request.user.is_anonymous:
            return redirect('/')

        # get object
        try:
            request_object = RequestModel.objects.get(id=id)
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
                    'mail': i.mail
                })
    
        # update context with new_data
        context.update({
            'results': results,
            'control_results': control_results,
            'results_bool': results_bool,
            'all_results_bool': all_results_bool,
            'control_results_bool': control_results_bool,
            'messages_bool': messages_bool,
            'messages': messages_struct
        })

        return render(
            request,
            'user/request_one/request_one.html',
            context=context
        )
