from django.shortcuts import (
    render,
    redirect
)
from app.models import RequestModel
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

        return render(
            request,
            'user/request_one/request_one.html',
            context=RequestsTableSerializer.get_data_for_one(
                RequestsSerializer(request_object)
            )
        )
