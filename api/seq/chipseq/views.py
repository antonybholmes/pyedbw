from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.persons.models import Person
from api.persons.serializers import PersonSerializer
from api import auth
import libhttp

from api.samples.models import SampleFile


def peaks_callback(key, person, user_type, id_map=None):
    id = id_map['id'][0]
    
    genome = id_map['g'][0]
    
    loc = libhttpdna.get_loc_from_params(id_map)
    
    if loc is None:
        return JsonResponse([], safe=False)
    
    mode = id_map['m'][0]    
    
    # Get the path location
     
    #sub_dirs = VFSFile.objects.filter(id=11244) #samplefile__sample__=id)
    sub_dirs = VFSFile.objects.filter(samplefile__sample=id)
    

    if len(sub_dirs) == 0:
        return JsonResponse([], safe=False)
        
    sub_dir = sub_dirs[0].path
        
    gei = something
    
    
    if 'bw' in id_map:
        bin_width = id_map['bw'][0]
    else:
        bin_width = 1000
        
    bcr = libgeb.from_gei(gei)
    
    locations = bcr.find(loc)
    
    return JsonResponse([{'id':id, 
        'l':loc.__str__(), 
        'bw':bin_width, 
        'mode':mode, 
        'c':locations.tolist()}], safe=False)    


def peaks(request):
    id_map = libhttp.ArgParser() \
        .add('id',-1) \
        .add('g','hg19') \
        .add('chr','chr3') \
        .add('s',187721377) \
        .add('e',187736497) \
        .add('bw',1000) \
        .add('m','count') \
        .parse(request)
    
    #return counts_callback(None, None, None, id_map=id_map)
    
    return auth.auth(request, peaks_callback, id_map=id_map)
