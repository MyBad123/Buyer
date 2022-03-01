from unittest import result
from django.shortcuts import render, redirect

from app.models import RequestModel, ResultModel
from app.serializers import ResultSerialzier, ForResultSerialzier


class Results:
    """views for result"""

    @staticmethod
    def get_result_page(request, pk):
        """get all results of request"""
        
        if request.user.is_anonymous:
            return redirect('/')

        # get object
        try:
            request_object = RequestModel.objects.get(id=pk)
        except RequestModel.DoesNotExist:
            return redirect('/')

        # work with context 
        context = {
            'name': request_object.name,
            'words': request_object.words
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

