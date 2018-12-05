from django.urls import path
from django.conf.urls import url

from api.genomic.elements import views

urlpatterns = [
    path('track', views.track, name='track'),
    path('search', views.search, name='search'),
]
