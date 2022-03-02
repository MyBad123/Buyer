from unittest import result
from django.shortcuts import render, redirect

from app.models import RequestModel, ResultModel
from app.serializers import ResultSerialzier, ForResultSerialzier


class Results:
    """views for result"""

    @staticmethod
    def control_user_and_id(request, pk):
        """control permissions """

        # control user
        if request.user.is_anonymous:
            return True

        # control id
        try:
            RequestModel.objects.get(id=pk)
        except RequestModel.DoesNotExist:
            return True

        return False

    @staticmethod
    def get_result_page(request, pk):
        """get all results of request"""
        
        # control permissions and pk
        if Results.control_user_and_id(request, pk):
            return redirect('/')
        else:
            request_object = RequestModel.objects.get(id=pk)

        # work with context 
        context = {
            'name': request_object.name,
            'words': request_object.words,
            'id': pk
        }

        # get all results(with serializer) and update context
        results = ResultModel.objects.filter(request=request_object)
        results_serializer = ForResultSerialzier(
            serializer=ResultSerialzier(results, many=True)
        )
        context.update({
            'results_serializer': results_serializer.get_data()
        })

        return render(
            request, 
            'user/request_one/all_results.html',
            context=context
        )

    @staticmethod
    def get_correct_result_page(request, pk):
        """get results for push mail"""

        # control permissions and pk
        if Results.control_user_and_id(request, pk):
            return redirect('/')
        else:
            request_object = RequestModel.objects.get(id=pk)

        # get objects and add data of this on context
        result_objects = ResultModel.objects.filter(
            request=request_object,
            status=True
        )
        context = {
            'name': request_object.name,
            'words': request_object.words,
            'id': pk
        }
        serializer = ForResultSerialzier(ResultSerialzier(
            result_objects, 
            many=True
        ))
        context.update({
            'results_serializer': serializer.get_control_data()
        })

        return render(
            request, 
            'user/request_one/all_control_results.html',
            context=context
        )

        

