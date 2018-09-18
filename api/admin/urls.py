from django.urls import path
from django.conf.urls import url

from api.admin import views

urlpatterns = [
    path('person', views.person, name='person'),
]
