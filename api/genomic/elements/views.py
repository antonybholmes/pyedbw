from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.samples.models import Sample
from api.persons.serializers import PersonSerializer
from api.genomic.elements.models import Element
from api.genomic.elements.serializers import ElementSerializer
from api import auth
from edbw import settings
import libhttp
import libhttpdna
import libgeb

def track_callback(key, person, user_type, id_map=None):
    id = id_map['id'][0]
    
    genome = id_map['g'][0]
    
    loc = libhttpdna.get_loc_from_params(id_map)
    
    if loc is None:
        return JsonResponse([], safe=False)
    
    bin_width = id_map['bw'][0]
    level = id_map['l'][0]
    
    # Get the path location
     
    #sub_dirs = VFSFile.objects.filter(id=11244) #samplefile__sample__=id)
    elements = Element.objects.filter(id=id)
    

    if len(elements) == 0:
        return JsonResponse([], safe=False)
        
    element = elements[0]
    
    bcr = libgeb.from_gei(settings.DATA_DIR + element.path)
    
    print(loc, level)
    
    elements = bcr.find(loc, level=level)
    
    els = []
    
    for element in elements:
        els.append(element.loc) #basic_json)
    
    return JsonResponse([{'id':id, 
        'loc':loc.__str__(), 
        'bw':bin_width,
        'e':els,
        'l':level}], safe=False)    


def track(request):
    id_map = libhttp.parse_params(request, {'id':-1, 
        'g':'hg19', 
        'chr':'chr10', 
        's':87500, 
        'e':88800, 
        'bw':1000,
        'l':'peak'})
    
    return auth.auth(request, track_callback, id_map=id_map)
    
    
def search_callback(key, person, user_type, id_map=None):
    id = id_map['id'][0]
     
    #sub_dirs = VFSFile.objects.filter(id=11244) #samplefile__sample__=id)
    elements = Element.objects.filter(sample_id=id)
    
    serializer = ElementSerializer(elements, many=True, read_only=True)
     
    return JsonResponse(serializer.data, safe=False)    


def search(request):
    id_map = libhttp.parse_params(request, {'id':-1})
    
    return auth.auth(request, search_callback, id_map=id_map)
