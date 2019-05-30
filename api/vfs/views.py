from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from api.vfs.models import VFSFile, VFSFileJson
from api.vfs.serializers import VFSFileSerializer
from api import auth, views
from api import libcollections
from edbw import settings
import libhttp

def ls_callback(key, person, user_type, id_map={}):
    #if 'parent' in id_map:
        #pid = id_map['parent'][0]
        #serializer = VFSFileSerializer(VFSFile.objects.filter(parent_id=pid), many=True, read_only=True)
    #else:
        #serializer = VFSFileSerializer(VFSFile.objects.order_by('id')[:100], many=True, read_only=True)
    
    #return JsonResponse(serializer.data, safe=False)
    
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = 1
    
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
    sortby = id_map['sortby']
    
    if 'parent' in id_map:
        pid = id_map['parent']
        rows = VFSFileJson.objects.filter(parent_id=pid).order_by(sortby).values('json')
    else:
        rows = VFSFileJson.objects.order_by(sortby).values('json')
    
    paginator = Paginator(rows, records)
    
    page_rows = paginator.get_page(page)
    
    if 'page' in id_map:
        return views.json_page_resp('files', page, paginator) #return JsonResponse({'page':page, 'pages':paginator.num_pages, 'files':[x['json'] for x in page_rows]}, safe=False)
    else:
        return views.json_resp(page_rows)


def ls(request):
    """
    List information about virtual files in the database.
    
    Parameters
    ----------
    request : Request
        If 'parent' is present as a GET param, restrict ls to a particular
        file, otherwise list all files.
    """
    
    id_map = libhttp.ArgParser() \
    .add('key') \
    .add('parent', default_value=None, arg_type=int) \
    .add('page', arg_type=int) \
    .add('records', default_value=100) \
    .add('sortby', default_value='id') \
    .parse(request)
    
    return auth.auth(request, ls_callback, id_map=id_map, pkey_only=False)


def path_callback(key, person, user_type, id_map={}):
    
    id = id_map['file'][0]
    
    file = VFSFile.objects.get(id=id)

    stack = libcollections.Stack()

    stack.push(file)

    go = True

    while go:
        pid = stack.peek().parent_id

        if pid == -1:
            go = False
            break

        # Keep going until the root is reached
        stack.push(VFSFile.objects.get(id=pid))
    
    if 'mode' in id_map and id_map['mode'][0] == 'str':
        return JsonResponse({'path': '/{}'.format('/'.join([vfs.name for vfs in stack.tolist()[1:]]))}, safe=False)
    else:
        serializer = VFSFileSerializer(stack.tolist(), many=True, read_only=True)
    
        return JsonResponse(serializer.data, safe=False)
    
    
def path(request):
    id_map = {}
    
    auth.parse_ids(request, 'file', id_map=id_map)
    auth.parse_params(request, 'mode', id_map=id_map)
 
    return auth.auth(request, path_callback, id_map=id_map)

