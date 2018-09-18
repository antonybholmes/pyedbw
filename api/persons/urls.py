from django.urls import path
from django.conf.urls import url

from api.persons import views

urlpatterns = [
    path('', views.persons, name='persons'),
]
