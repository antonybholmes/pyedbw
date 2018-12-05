from django.urls import path
from django.conf.urls import url

from api.ucsc import views

urlpatterns = [
    path('tracks', views.tracks, name='tracks'),
]
