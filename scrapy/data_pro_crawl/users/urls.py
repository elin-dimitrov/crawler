from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('session', views.UsersSession.as_view(), name='session'),
]
