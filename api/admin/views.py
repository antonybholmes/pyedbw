from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.persons.models import Person
from api.admin.serializers import PersonSerializer
from api import auth

def person_callback(key, person, user_type, id_map):
    serializer = PersonSerializer(person, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)


def person(request):
    """
    Display Person
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    key = request.GET['key']
    
    return auth.key_auth(key, person, user_type_callback)
    
    
