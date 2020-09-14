from django.urls import path
from . import views
#from rest_framework.authtoken import views 


app_name = 'ministers'

urlpatterns = [
    path('', views.Politician.as_view(), name='ministers'),
    path('data', views.ImportData.as_view(), name='data_import'),
]
