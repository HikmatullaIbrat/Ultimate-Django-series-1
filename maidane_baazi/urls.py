
from django.urls import path, re_path
from . import views


#URL Conf

urlpatterns = [
    re_path('salaam/', views.say_salaam)
    
]
