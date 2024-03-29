from django.urls import path
from . import views

urlpatterns = [
    path('user-signup/', views.UserSignup.as_view()),
    path('user-login/', views.UserLogin.as_view()),
    ]