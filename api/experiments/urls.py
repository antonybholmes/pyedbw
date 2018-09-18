from django.urls import path
from django.conf.urls import url

from api.experiments import views

urlpatterns = [
    path('', views.experiments, name='experiments'),
]
