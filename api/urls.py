from django.urls import path
from django.conf.urls import url
from django.urls import include
from api import views

urlpatterns = [
    path('types/', include('api.types.urls')),
    path('experiments/', include('api.experiments.urls')),
    path('samples/', include('api.samples.urls')),
    path('persons/', include('api.persons.urls')),
    path('vfs/', include('api.vfs.urls')),
    path('download/', include('api.download.urls')),
    path('seq/', include('api.seq.urls')),
    path('ucsc/', include('api.ucsc.urls')),
    path('groups/', include('api.groups.urls')),
    path('account/', include('api.account.urls')),
    path('admin/', include('api.admin.urls')),
    path('about', views.about, name='about'),
]
