from django.urls import path
from django.conf.urls import url

from api.groups import views

urlpatterns = [
    path('', views.groups, name='groups'),
]
