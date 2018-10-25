from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import libhttp
from api.ucsc.models import Track
from api.ucsc.serializers import TrackSerializer
from api import auth

def hex_to_rgb(value):
    value = value.lstrip('#')
    #return tuple(int(value[i:(i + 2)], 16) for i in range(0, 6, 2))
    return ','.join([str(int(value[i:(i + 2)], 16)) for i in range(0, 6, 2)])
    
  
def tracks_callback(key, person, user_type, id_map={}):
    ids = id_map['id']
    colors = id_map['c'] #[hex_to_rgb(c) for c in id_map['c']]
    
    while len(colors) < len(ids):
        colors.append(colors[0])
    
    mode = id_map['mode'][0]
    
    tracks = Track.objects.filter(sample_id__in=ids) #Track.objects.all() #(id__in=ids)
    
    if (mode == 'json'):
        serializer = TrackSerializer(tracks, many=True, read_only=True)
    
        return JsonResponse(serializer.data, safe=False)
    else:
        output = []
        
        for i in range(0, len(ids)):
            track = tracks[i]
            color = colors[i]
           
            name = track.sample.name
            l = 'track type=bigWig name="{}" description="{}" visibility="full" color={} bigDataUrl={}'.format(name, name, color, track.url)
            output.append(l)
            
        return HttpResponse("\n".join(output), content_type='text/plain')

def tracks(request):
    id_map = libhttp.parse_params(request, {'id':-1, 'key':'', 'mode':'text', 'c':'255,0,0'})
 
    return auth.auth(request, tracks_callback, id_map=id_map)
