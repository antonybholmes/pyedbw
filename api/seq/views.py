from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.persons.models import Person
from api.persons.serializers import PersonSerializer
from api import auth
from edbw import settings

import re
import sys

import os
import libseq
import libdna

from api.samples.models import SampleFile
from api.vfs.models import VFSFile


def counts_callback(key, person, user_type, id_map={}):
    if 'id' not in id_map:
        return JsonResponse([], safe=False)
        
    id = id_map['id'][0]
       
    if 'loc' not in id_map or not libdna.is_loc(id_map['loc'][0]):
        return JsonResponse([], safe=False)
        
    loc = id_map['loc'][0]
    
    loc = libdna.parse_loc(loc)
    
    if 'g' not in id_map:
        return JsonResponse([], safe=False)
        
    genome = id_map['g'][0]
    
    # Get the path location
     
    #sub_dirs = VFSFile.objects.filter(id=11244) #samplefile__sample__=id)
    sub_dirs = VFSFile.objects.filter(samplefile__sample=id)
    

    if len(sub_dirs) == 0:
        return JsonResponse([], safe=False)
        
    sub_dir = sub_dirs[0].path
        
    dir = settings.DATA_DIR + sub_dir #os.path.join(settings.SEQ_DIR, sub_dir) #str(id))
    
    if 'bw' in id_map:
        bin_width = id_map['bw'][0]
    else:
        bin_width = 100
        
    bcr = libseq.BinCountReader(dir, genome=genome)
    locations = bcr.get_counts(loc, bin_width=bin_width)
    
    return JsonResponse([{'id' : id, 'l' : loc.__str__(), 'bw' : bin_width, 'c' : locations.tolist()}], safe=False)    


def counts(request):
    id_map = {}
    
    #auth.parse_ids(request, {'bw' : 100}, id_map=id_map)
    auth.parse_params(request, 'id', 'g', 'loc', {'bw' : 100}, id_map=id_map)
    
    #return counts_callback(None, None, None, id_map=id_map)
    
    return auth.auth(request, counts_callback, id_map=id_map)
    
    
def mapped_callback(key, person, user_type, id_map={}):
    if 'id' not in id_map:
        return JsonResponse([], safe=False)
        
    id = id_map['id'][0]
    
    # Get the path location
     
    #sub_dirs = VFSFile.objects.filter(id=11244) #samplefile__sample__=id)
    sub_dirs = VFSFile.objects.filter(samplefile__sample=id)
    
    if len(sub_dirs) == 0:
        return JsonResponse([], safe=False)
        
    sub_dir = sub_dirs[0].path
        
    file = settings.DATA_DIR + sub_dir + '/mapped_reads_count.txt' #os.path.join(settings.SEQ_DIR, sub_dir) #str(id))
    
    
    
    if os.path.isfile(file):
        f = open(file, 'r')
        count = int(f.readline().strip())
        f.close()
    else:
        count = 0
        
    return JsonResponse([count], safe=False)    


def mapped(request):
    id_map = {}
    
    #auth.parse_ids(request, {'bw' : 100}, id_map=id_map)
    auth.parse_params(request, 'id', id_map=id_map)
    
    #return counts_callback(None, None, None, id_map=id_map)
    
    return auth.auth(request, mapped_callback, id_map=id_map)
        
    
def data_type(request):
    return JsonResponse(['bc'], safe=False)
