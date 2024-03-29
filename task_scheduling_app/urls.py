from django.urls import path
from . import views

urlpatterns = [
    path('create-task/', views.CreateTask.as_view()),
    path('get-task/', views.GetTask.as_view()),
    ]