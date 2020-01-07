from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import Group
from api.groups.serializers import GroupSerializer
from api import auth


def _groups_callback(key, user, user_type, id_map={}):
    if user_type != 'Normal':
        groups = Group.objects.all().order_by('name')
    else:
        print(user)
        groups = user.groups.all() #Group.objects.filter(login_user_groups__user_id=user.id).order_by('name')
    
    #serializer = GroupSerializer(groups, many=True, read_only=True)
    
    data = []
    
    for g in groups:
        data.append({'id':g.id, 'n':g.name, 'c':'#000000'})
    
    return JsonResponse(data, safe=False) #views.json_resp(paginator.get_page(1))
    #return JsonResponse(serializer.data, safe=False)
    
    
def groups(request):
    id_map = {}
    
    return auth.auth(request, _groups_callback, id_map=id_map)
