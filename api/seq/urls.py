from django.urls import path
from django.conf.urls import url
from django.urls import include
from api.seq import views


urlpatterns = [
    path('chipseq/', include('api.seq.chipseq.urls')),
    path('counts', views.counts, name='counts'),
    path('mapped', views.mapped, name='mapped'),
    path('type', views.data_type, name='type'),
]
