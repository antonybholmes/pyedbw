from django.urls import path
from django.conf.urls import url

from api.download import views

urlpatterns = [
    path('files', views.files, name='files'),
]
