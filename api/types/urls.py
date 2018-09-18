from django.urls import path
from django.conf.urls import url

from api.types import views

urlpatterns = [
    path('organisms', views.organisms, name='organisms'),
    path('tags', views.tags, name='tags'),
    path('genomes', views.genomes, name='genomes'),
    path('roles', views.roles, name='roles'),
    path('data', views.data, name='data'),
]
