from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.groups.models import Group
from api.groups.serializers import GroupSerializer
from api import auth


def _groups_callback(key, person, user_type, id_map={}):
    if user_type != 'Normal':
        groups = Group.objects.all().order_by('name')
    else:
        groups = Group.objects.filter(groupperson__person_id=person.id).order_by('name')
    
    serializer = GroupSerializer(groups, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    
    
def groups(request):
    id_map = {}
    
    return auth.auth(request, _groups_callback, id_map=id_map)
