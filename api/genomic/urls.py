from django.urls import path
from django.conf.urls import url
from django.urls import include

urlpatterns = [
    path('elements/', include('api.genomic.elements.urls')),
]
