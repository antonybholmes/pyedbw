from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
import libhttp
from api.ucsc.models import Track
from api.ucsc.serializers import TrackSerializer
from api import auth

  
def tracks_callback(key, person, user_type, id_map={}):
    ids = id_map['id']
    mode = id_map['mode'][0]
    
    tracks = Track.objects.filter(sample_id__in=ids) #Track.objects.all() #(id__in=ids)
    
    
    if (mode == 'json'):
        serializer = TrackSerializer(tracks, many=True, read_only=True)
    
        return JsonResponse(serializer.data, safe=False)
    else:
        output = []
        
        for track in tracks:
            l = 'track type=bigWig name="{}" description="{}" visibility="full" bigDataUrl={}'.format(track.name, track.name, track.url)
            output.append(l)
            
        return HttpResponse("\n".join(output), content_type='text/plain')

def tracks(request):
    id_map = libhttp.parse_params(request, {'id':-1, 'key':'', 'mode':'text'})
 
    return auth.auth(request, tracks_callback, id_map=id_map)
