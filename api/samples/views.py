from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.models import Tag
from api.persons.models import Person
from api.persons.serializers import PersonSerializer
from api.vfs.models import VFSFile
from api.vfs.serializers import VFSFileSerializer
from api.samples.models import Sample, TagSampleSearch, TagKeywordSearch, SampleFile, SampleTag, SampleIntTag, SampleFloatTag
from api.samples.serializers import SampleSerializer, SampleTagSerializer
from api import auth, libsearch, libcollections

  
def sample_callback(key, person, user_type, id_map={}):
    if 'sample' in id_map:
        ids = id_map['sample']
        
        if user_type != 'Normal':
            samples = Sample.objects.filter(id__in=ids)
        else:
            samples = Sample.objects.filter(groups__person__id=person.id, id__in=ids)
    else:
        # return all samples
        
        #samples = Sample.objects.all(), many=True, read_only=True)
        
        if user_type != 'Normal':
            samples = Sample.objects.all()
        else:
            # Normal users are filtered by the groups they belong to
            samples = Sample.objects.filter(groups__person__id=person.id)
    
    serializer = SampleSerializer(samples, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def samples(request):
    id_map = auth.parse_ids(request, 'sample')
 
    return auth.auth(request, sample_callback, id_map=id_map)


def persons_callback(key, person, user_type, id_map={}):
    persons = Person.objects.filter(sampleperson__sample__in=id_map['sample'])
    
    serializer = PersonSerializer(persons, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def persons(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, persons_callback, id_map=id_map, check_for={'sample'})
    
    
def tags_callback(key, person, user_type, id_map={}):
    
    ret = []
    
    if 'tag' in id_map:
        tags = SampleTag.objects.filter(sample__in=id_map['sample'], tag__in=id_map['tag'])
        append_tags(tags, ret)
            
        tags = SampleIntTag.objects.filter(sample__in=id_map['sample'], tag__in=id_map['tag'])
        append_tags(tags, ret)
        
        tags = SampleFloatTag.objects.filter(sample__in=id_map['sample'], tag__in=id_map['tag'])
        append_tags(tags, ret)
    else:
        tags = SampleTag.objects.filter(sample__in=id_map['sample'])
        append_tags(tags, ret)   
        
        tags = SampleIntTag.objects.filter(sample__in=id_map['sample'])
        append_tags(tags, ret)
        
        tags = SampleFloatTag.objects.filter(sample__in=id_map['sample'])
        append_tags(tags, ret)
    
    # Rather than using a serializer, here we combine records into
    # a list of dicts and use that to generate JSON directly
    serializer = SampleTagSerializer(tags, many=True, read_only=True)
    
    return JsonResponse(ret, safe=False)


def append_tags(sample_tags, ret):
    for sample_tag in sample_tags:
        ret.append({'id' : sample_tag.tag.id, 'v' : sample_tag.value})


def tags(request):
    id_map = {}
    auth.parse_ids(request, 'sample', id_map=id_map)
    auth.parse_ids(request, 'tag', id_map=id_map)
    
    return auth.auth(request, tags_callback, id_map=id_map, check_for={'sample'})
       
    
def geo_callback(key, person, user_type, id_map={}):
    return JsonResponse([], safe=False)    


def geo(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, geo_callback, id_map=id_map)
    

def file_callback(key, person, user_type, id_map={}):
    files = VFSFile.objects.filter(samplefile__sample__in=id_map['sample'])
    
    serializer = VFSFileSerializer(files, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def files(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, file_callback, id_map=id_map)
    
    
def search_callback(key, person, user_type, id_map={}):
    # The search query
    
    if 'q' in id_map:
        # If query exists use it.
        q = id_map['q'][0]
    else:
        q = ''
    
    search_queue = libsearch.parse_query(q)
    
    tag = Tag.objects.get(name=id_map['tag'][0])
    
    #samples = Sample.objects.filter(tagsamplesearch__tag_keyword_search__keyword__name__contains=q).filter(tagsamplesearch__tag_keyword_search__tag__id=tag.id).distinct()
    
    samples = search_samples(tag, search_queue)
    
    if 'type' in id_map:
        samples = samples.filter(expression_type_id__in=id_map['type'])
    
    serializer = SampleSerializer(samples, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)


def search_samples(tag, search_queue, max_count=100):
    if len(search_queue) == 0:
        # If there is no query, default to return 100 results ordered 
        # by name
        return Sample.objects.order_by('name')[:10]

    stack = libcollections.Stack()

    for e in search_queue:
        if e.op == 'MATCH':
            samples = Sample.objects.filter(tagsamplesearch__tag_keyword_search__keyword__name__contains=e.text)
                .filter(tagsamplesearch__tag_keyword_search__tag__id=tag.id).distinct()
    
            stack.push(samples)
        elif e.op == 'AND':
            stack.push(stack.pop().intersection(stack.pop())) #(tempStack.pop(), tempStack.pop()));
        elif e.op == 'OR':
            stack.push(stack.pop().union(stack.pop()))
        else:
            pass

    return stack.pop()


def search(request):
    id_map = auth.parse_params(request, 'q', {'tag':'/All'}, 'type')
    
    return auth.auth(request, search_callback, id_map=id_map)
    
