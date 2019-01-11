from django.urls import path
from django.conf.urls import url

from api.samples import views

urlpatterns = [
    path('', views.samples, name='samples'),
    path('search', views.search, name='search'),
    path('sets', views.sets, name='sets'),
    path('persons', views.persons, name='persons'),
    path('tags', views.tags, name='tags'),
    path('geo', views.geo, name='geo'),
    path('files', views.files, name='files'),
]
