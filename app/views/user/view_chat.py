from django.shortcuts import render, redirect

class ChatViews:
    """methods for chat"""

    @staticmethod
    def get_page(request):
        """get all message with mail"""

        # control auth
        if request.user.is_anonymous:
            return redirect('/')

        # control new messages
        

        return render(request, 'user/chat/chat.html')
        