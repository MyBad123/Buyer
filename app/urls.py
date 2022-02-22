from django.urls import path

from .views.user.views_user import *
from .views.user.view_thanks import *
from .views.db.views_db import *
from .views.admin.views_admin import *
from .views.user.view_request_one import *

urlpatterns = [
    path('admin/', AdminMethods.get_admin_page),
    path('user-add-page/', AdminMethods.get_new_user_page),
    path('user-add/', AdminMethods.new_user),
    path('update-user-page/', AdminMethods.update_user_page),
    path('update-user/', AdminMethods.update_user),
    path('delete-user/', AdminMethods.delete_user),
    path('db/', DbMethods.get_db_page),
    path('delete-db/', DbMethods.delete),
    path('create-db/', DbMethods.create),
    path('', AuthMethods.auth_page),
    path('auth/', AuthMethods.auth),
    path('exit/', AuthMethods.exit),
    path('user-page/', UserMethods.get_users_page),
    path('user-new-request-page/', UserMethods.new_request_page),
    path('user-new-request/', UserMethods.new_request),
    path('user-thanks/', RequestThanks.get_thanks_page),
    path('request-page/', RequestOneView.no_request_redirect),
    path('request-page/<int:id>/', RequestOneView.get_request)
]
