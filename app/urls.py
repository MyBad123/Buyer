from django.urls import path

from app.views.user.views_user import *
from app.views.user.view_thanks import *
from app.views.db.views_db import *
from app.views.admin.views_admin import *
from app.views.user.view_request_one import *
from app.views.user.chat.view_chat import *
from app.views.user.view_result import *
from app.views.user.view_csv import *
from app.views.markup_doc.view_markup_doc import *
from app.views.admin.views_company_admin import *


urlpatterns = [
    path('admin/', AdminMethods.get_admin_page),
    path('user-add-page/', AdminMethods.get_new_user_page),
    path('user-add/', AdminMethods.new_user),
    path('update-user-page/', AdminMethods.update_user_page),
    path('update-user/', AdminMethods.update_user),
    path('delete-user/', AdminMethods.delete_user),
    path('admin-get-all-companies/', AdminCompaniesView.as_view()),
    path('admin-create-company/', AdminCompanyCreate.as_view()),
    path('admin-update-company/', AdminUpdateCompanyView.as_view()),
    path('db/', DbView.get_db_page),
    path('delete-db/', DbView.delete),
    path('create-db/', DbView.create),
    path('', AuthMethods.auth_page),
    path('auth/', AuthMethods.auth),
    path('exit/', AuthMethods.exit),
    path('user-page/', UserMethods.get_users_page),
    path('user-page-api/', UserMethods.get_users_page_api),
    path('user-new-request-page/', UserMethods.new_request_page),
    path('user-new-request/', UserMethods.new_request),
    path('user-thanks/', RequestThanks.get_thanks_page),
    path('request-page/', RequestOneView.no_request_redirect),
    path('request-page/<int:id>/', RequestOneView.get_request),
    path('request-page-delete/<int:id>/', RequestOneView.delete_request),
    path('results/<int:pk>/', ResultsView.get_result_page),
    path('control-results/<int:pk>/', ResultsView.get_correct_result_page),
    path('control-results-send-message/', ResultsView.send_messages),
    path('control-results-send-message-thanks/<int:pk>/', ResultsView.thanks_after_message),

    # requests for chat
    path('chat/', ChatViews.get_page),
    path('chat/<int:pk>/', ChatViews.get_page_with_mail),
    path('get-page-send-mesage/<int:pk>/', ChatViews.get_page_send_mesage),
    path('chat-get-send-message/<int:pk>/', ChatViews.send_message),
    path('chat-thanks/<int:pk>/', ChatViews.send_thank),
    path('chat-after-parsing/<int:pk>/', ChatViews.get_page_after_parsing),

    # for getting csv
    path('get-csv/', CsvView.get_page),
    path('set-csv/', CsvView.set_csv),
    path('get-csv-logs/', CsvView.get_logs),
    path('set-csv-logs/', CsvView.set_logs),
    path('get-csv-file/', CsvView.get_csv_file),
    path('create-markup-doc/', MarkupDoc.create_markup_doc),
]
