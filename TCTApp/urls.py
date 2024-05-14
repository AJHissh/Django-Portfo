from django.urls import path, include, re_path
from django.conf import settings 
from . import views
from .views import *
from .models import *

##----------------------------------------------##

## APP 1 URLS ##

##----------------------------------------------##


## Determines which view from views.py is returned when a user hits a certain url ## 
urlpatterns = [
    path("", views.index, name="index"),
    path("test", views.test, name='test'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),  
    path("view_records", views.view_records, name="view_records"),
    path("profile", views.profile_view, name="profile"),
    path("request_edit/", views.request_edit, name="request_edit"),
    path("resume_tasks/", views.resume_tasks, name="resume_tasks"),
    path('request_edit/<uuid:record_id>/', views.request_edit, name='request_edit_with_id'),
    path('resume_tasks/<uuid:record_id>/', views.resume_tasks, name='resume_tasks_with_id'),
    path('view_history', views.view_history, name='view_history'),
    path('view_history/<uuid>/', views.view_history, name='view_history'),
    path('task_page', views.task_page, name='task_page'),
    path("admin_view_records", views.admin_view_records, name="admin_view_records"),
    path("admin_date_filter", views.admin_date_filter, name="admin_date_filter"),
    path("admin_edit_records", views.admin_edit_records, name="admin_edit_records"),
    path('admin_edit_records/<uuid:record_id>/', views.admin_edit_records, name='admin_edit_with_id'),
    path("admin_view_history", views.admin_view_history, name="admin_view_history"),
    path("admin_view_change_requests", views.admin_view_change_requests, name="admin_view_change_requests"),
    path("admin_view_change_requests_completion", views.admin_view_change_requests_completion, name="admin_view_change_requests_completion"),
    path("admin_view_change_requests_completion/<uuid:record_id>/", views.admin_view_change_requests_completion, name="admin_view_change_requests_completion"),
    path('download_records', views.download_records, name='download_records'),
    path('Categoryone_download_records', views.Categoryone_download_records, name='Categoryone_download_records'),
    path('Categorytwo_download_records', views.Categorytwo_download_records, name='Categorytwo_download_records'),
    path('download_records_all_version', views.download_records_all_version, name='download_records_all_version'),
    path('download-resume/', download_resume, name='download_resume'),
    path("start_Categoryone_task", views.start_Categoryone_task, name="start_Categoryone_task"),
    path("start_Categoryone_task2", views.start_Categoryone_task2, name="start_Categoryone_task2"),
    path("start_Categoryone_task3", views.start_Categoryone_task3, name="start_Categoryone_task3"),

] 

##----------------------------------------------##

## END APP 1 URLS ##

##----------------------------------------------##
