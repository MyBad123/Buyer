from django.shortcuts import render, redirect

class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request, id):
        

        return render(request, 'user/chat/chat.html')