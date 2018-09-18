from django.urls import path
from django.conf.urls import url

from api.account import views

urlpatterns = [
    path('groups', views.groups, name='groups'),
]
