from django.urls import path
from django.conf.urls import url

from api.vfs import views

urlpatterns = [
    path('ls', views.ls, name='ls'),
    path('path', views.path, name='path'),
]
