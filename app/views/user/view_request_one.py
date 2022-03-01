from unittest import result
from django.shortcuts import (
    render,
    redirect
)
from app.models import RequestModel, ResultModel
from app.serializers import (
    RequestsSerializer,
    RequestsTableSerializer,
    ResultSerialzier,
    ForResultSerialzier
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

        # update context with RequestTable
        results = ResultModel.objects.filter(
            request=request_object, 
            status=True
        )
        results_serializer = ForResultSerialzier(
            ResultSerialzier(results, many=True)
        )
        context.update({
            'results': results_serializer.get_data()
        })

        # get number of results
        results = len(ResultModel.objects.filter(
            request=request_object
        ))
        control_results = len(ResultModel.objects.filter(
            request=request_object,
            status=True
        ))


        if request_object.datetime_yandex_finished is None:
            for_result = True
        else: 
            for_result = False
        
        return render(
            request,
            'user/request_one/request_one.html',
            context=context
        )
