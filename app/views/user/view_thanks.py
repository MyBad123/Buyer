from django.shortcuts import render


class RequestThanks:
    @staticmethod
    def get_thanks_page(request):
        return render(request, 'user/request/thanks.html')

