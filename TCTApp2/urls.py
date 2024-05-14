from django.urls import path, include, re_path
from . import views

app_name = 'TCTApp2'

urlpatterns = [
    path("start_Categorytwo_task/", views.start_Categorytwo_task, name="start_Categorytwo_task"),
    path("start_Categorytwo_task2/", views.start_Categorytwo_task2, name="start_Categorytwo_task2"),
    path("start_Categorytwo_task3/", views.start_Categorytwo_task3, name="start_Categorytwo_task3"),
]




