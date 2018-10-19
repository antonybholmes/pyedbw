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
import struct
import os
import libseq
import libdna
import libhttp
import libhttpdna

from api.samples.models import SampleFile
from api.vfs.models import VFSFile


def counts_callback(key, person, user_type, id_map=None):
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
        
    dir = settings.DATA_DIR + sub_dir #os.path.join(settings.SEQ_DIR, sub_dir) #str(id))
    
    if 'bw' in id_map:
        bin_width = id_map['bw'][0]
    else:
        bin_width = 100
        
    bcr = libseq.BinCountReader(dir, genome=genome, mode=mode)
    locations = bcr.get_counts(loc, bin_width=bin_width)
    
    return JsonResponse([{'id':id, 
        'l':loc.__str__(), 
        'bw':bin_width, 
        'mode':mode, 
        'c':locations.tolist()}], safe=False)    


def counts(request):
    id_map = libhttp.parse_params(request, {'id':-1, 
        'g':'grch38', 
        'chr':'chr3', 
        's':187721377, 
        'e':187736497, 
        'bw':100,
        'm':'count'})
    
    #return counts_callback(None, None, None, id_map=id_map)
    
    return auth.auth(request, counts_callback, id_map=id_map)
    
    
def mapped_callback(key, person, user_type, id_map={}):
    id = id_map['id'][0]
    
    # Get the path location
     
    sub_dirs = VFSFile.objects.filter(samplefile__sample=id)
    
    if len(sub_dirs) == 0:
        return JsonResponse(['No dirs'], safe=False)
        
    genome = id_map['g'][0]
    
    mode = id_map['m'][0]
    
    #bin_width = id_map['bw'][0]
        
    #if bin_width not in libseq.POWER:
    #    return JsonResponse(['p ' + str(bin_width)], safe=False)
        
    #power = libseq.POWER[bin_width]
        
    sub_dir = sub_dirs[0].path
        
    file = settings.DATA_DIR + sub_dir + '/reads.{}.{}.bc'.format(genome, mode) #'/mapped_reads_count.txt' #os.path.join(settings.SEQ_DIR, sub_dir) #str(id))
    
    
    
    if os.path.isfile(file):
        #f = open(file, 'r')
        #count = int(f.readline().strip())
        #f.close()
        f = open(file, 'rb')
        count = struct.unpack('>I', f.read(4))[0] #int(f.readline().strip())
        f.close()
    else:
        count = 0
    
    #count = file
    
    return JsonResponse([count], safe=False)    


def mapped(request):
    id_map = libhttp.parse_params(request, {'id':-1, 'g':'grch38', 'm':'count'})
    
    return auth.auth(request, mapped_callback, id_map=id_map)
        
    
def data_type(request):
    return JsonResponse(['bc'], safe=False)
