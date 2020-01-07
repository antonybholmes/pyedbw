from django.urls import path
from django.conf.urls import url

from api.users import views

urlpatterns = [
    path('', views.users, name='users'),
]
