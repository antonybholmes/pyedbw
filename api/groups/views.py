from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.groups.models import Group
from api.groups.serializers import GroupSerializer
from api import auth


def groups_callback(key, person, user_type, id_map={}):
    serializer = GroupSerializer(Group.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    
    
def groups(request):
    id_map = {}
    
    return auth.auth(request, groups_callback, id_map=id_map)



def samples_callback(key, person, user_type, id_map={}):
    serializer = GroupSerializer(Group.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    
    
def samples(request):
    id_map = {}
    
    return auth.auth(request, sample_groups_callback, id_map=id_map)

