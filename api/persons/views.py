from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.persons.models import Person
from api.persons.serializers import PersonSerializer
from api import auth


def persons_callback(key, person, user_type, id_map={}):
    if 'id' in id_map:
        ids = id_map['id']
        
        samples = Person.objects.filter(id__in=ids)
    else:
        samples = Person.objects.all()
    
    serializer = PersonSerializer(samples, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def persons(request):
    id_map = auth.parse_ids(request, 'id')
 
    return auth.auth(request, persons_callback, id_map=id_map)
