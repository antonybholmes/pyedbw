from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.models import Tag
from api.experiments.models import Experiment
from api.experiments.serializers import ExperimentSerializer
from api import auth

  
def experiments_callback(key, person, user_type, id_map={}):
    if 'id' in id_map:
        ids = id_map['id']
        
        experiments = Experiment.objects.filter(id__in=ids)
    else:
        experiments = Experiment.objects.all()
    
    serializer = ExperimentSerializer(experiments, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def experiments(request):
    id_map = auth.parse_ids(request, 'id')
 
    return auth.auth(request, experiments_callback, id_map=id_map)
