from django.urls import path

from .views.user.views_user import *
from .views.user.view_thanks import *
from .views.db.views_db import *
from .views.admin.views_admin import *
from .views.user.view_request_one import *
from .views.user.view_chat import *
from .views.user.view_result import *

urlpatterns = [
    path('admin/', AdminMethods.get_admin_page),
    path('user-add-page/', AdminMethods.get_new_user_page),
    path('user-add/', AdminMethods.new_user),
    path('update-user-page/', AdminMethods.update_user_page),
    path('update-user/', AdminMethods.update_user),
    path('delete-user/', AdminMethods.delete_user),
    path('db/', DbView.get_db_page),
    path('delete-db/', DbView.delete),
    path('create-db/', DbView.create),
    path('', AuthMethods.auth_page),
    path('auth/', AuthMethods.auth),
    path('exit/', AuthMethods.exit),
    path('user-page/', UserMethods.get_users_page),
    path('user-new-request-page/', UserMethods.new_request_page),
    path('user-new-request/', UserMethods.new_request),
    path('user-thanks/', RequestThanks.get_thanks_page),
    path('request-page/', RequestOneView.no_request_redirect),
    path('request-page/<int:id>/', RequestOneView.get_request),
    path('results/<int:pk>/', ResultsView.get_result_page),
    path('control-results/<int:pk>/', ResultsView.get_correct_result_page),
    path('control-results-send-message/', ResultsView.send_messages),
    path('chat/', ChatViews.get_page),
    path('chat/<int:pk>/', ChatViews.get_page_with_mail),
    path('push-message/', ChatViews.push_message)
]
