from django.urls import path
from django.conf.urls import url

from api.seq.chipseq import views

urlpatterns = [
    path('peaks', views.peaks, name='peaks'),
]
