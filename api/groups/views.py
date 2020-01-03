from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from api.groups.models import Group
from api.groups.serializers import GroupSerializer
from api import auth, views
from edbw import settings
import libhttp


def groups_callback(key, person, user_type, id_map={}):
    #serializer = GroupSerializer(Group.objects.all(), many=True, read_only=True)
    #return JsonResponse(serializer.data, safe=False)
    
    #print([x['json'] for x in GroupJson.objects.all().values('json')])
    
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = -1
    
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
    
    rows = Group.objects.all().values('json')
    
    paginator = Paginator(rows, records)
     
    if page > 0:
        return views.json_page_resp('groups', page, paginator) #JsonResponse({'page':page, 'pages':paginator.num_pages, 'groups':[x['json'] for x in page_rows]}, safe=False)
    else:
        return views.json_resp(paginator.get_page(1))
    
    
def groups(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .parse(request)
    
    return auth.auth(request, groups_callback, id_map=id_map)



#def samples_callback(key, person, user_type, id_map={}):
    ##serializer = GroupSerializer(Group.objects.all(), many=True, read_only=True)
    ##return JsonResponse(serializer.data, safe=False)
    
    #return JsonResponse(Group.objects.all().values('json'), safe=False)
    
    
#def samples(request):
    #id_map = {}
    
    #return auth.auth(request, sample_groups_callback, id_map=id_map)

