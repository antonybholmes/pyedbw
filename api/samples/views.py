from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.models import Tag
from api.persons.models import Person
from api.persons.serializers import PersonSerializer
from api.vfs.models import VFSFile
from api.vfs.serializers import VFSFileSerializer
from api.samples.models import Sample, SampleTags, TagSampleSearch, TagKeywordSearch, SampleFile, SampleTag #, SampleIntTag, SampleFloatTag
from api.samples.serializers import SampleSerializer #, SampleTagSerializer
from api import auth, libsearch, libcollections
import libhttp
import collections

  
def _sample_callback(key, person, user_type, id_map={}):
    if 'sample' in id_map:
        ids = id_map['sample']
        
        if user_type != 'Normal':
            samples = Sample.objects.filter(id__in=ids).order_by('name')
        else:
            samples = Sample.objects.filter(groups__person__id=person.id, id__in=ids).distinct().order_by('name')
    else:
        # return all samples
        
        #samples = Sample.objects.all(), many=True, read_only=True)
        
        if user_type != 'Normal':
            samples = Sample.objects.all()
        else:
            # Normal users are filtered by the groups they belong to
            samples = Sample.objects.filter(groups__person__id=person.id)
    
    print(id_map['sample'])
    
    serializer = SampleSerializer(samples, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)


def samples(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('sample', None, int, multiple=True) \
        .parse(request)
        
    #id_map = auth.parse_ids(request, 'sample')
 
    return auth.auth(request, _sample_callback, id_map=id_map)


def _persons_callback(key, person, user_type, id_map={}):
    persons = Person.objects.filter(sampleperson__sample__in=id_map['sample'])
    
    serializer = PersonSerializer(persons, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def persons(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, _persons_callback, id_map=id_map, check_for={'sample'})
    

def _append_tags(sample_tags, ret):
    for sample_tag in sample_tags:
        tag = {} #collections.OrderedDict()
        
        tag['id'] = sample_tag.tag.id
        
        if sample_tag.tag_type.id == 2:
            tag['v'] = sample_tag.int_value
        elif sample_tag.tag_type.id == 3:
            tag['v'] = sample_tag.float_value
        else:
            tag['v'] = sample_tag.str_value
            
        ret.append(tag)
        
def _append_tags(sample_tags, ret):
    for sample_tag in sample_tags:
        tag = {} #collections.OrderedDict()
        
        tag['id'] = sample_tag.tag.id
        
        if sample_tag.tag_type.id == 2:
            tag['v'] = sample_tag.int_value
        elif sample_tag.tag_type.id == 3:
            tag['v'] = sample_tag.float_value
        else:
            tag['v'] = sample_tag.str_value
            
        ret.append(tag)
        
def _tags_to_str(sample_tags):
    ret = '' #tag:value\n'
    
    for sample_tag in sample_tags:
        if sample_tag.tag_type.id == 2:
            v = sample_tag.int_value
        elif sample_tag.tag_type.id == 3:
            v = sample_tag.float_value
        else:
            v = sample_tag.str_value
            
        ret += '{}:{}\n'.format(sample_tag.tag.id, v)
    
    return ret
    
def _json_to_str(tags):
    ret = ''
    
    for tag in tags.values('data')[0]['data']:
        print(tag)
        ret += '{}:{}\n'.format(tag['id'], tag['v'])
    
    return ret

def _tags_callback(key, person, user_type, id_map={}):
    tags = SampleTags.objects.filter(sample_id=id_map['sample'])
    
    if id_map['format'] == 'text':
        return HttpResponse(_json_to_str(tags), content_type='text/plain; charset=utf8')
    else:
        #print(tags.values('data')[0]['data'][0]['id'])

        return JsonResponse(tags.values('data')[0]['data'], safe=False)





def tags(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('sample', arg_type=int) \
        .add('tag', arg_type=int) \
        .add('format', 'json') \
        .parse(request)
    
    return auth.auth(request, _tags_callback, id_map=id_map, check_for={'sample'})
       
    
def geo_callback(key, person, user_type, id_map={}):
    return JsonResponse([], safe=False)    


def geo(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, geo_callback, id_map=id_map)
    

def _file_callback(key, person, user_type, id_map={}):
    files = VFSFile.objects.filter(samplefile__sample__in=id_map['sample'])
    
    serializer = VFSFileSerializer(files, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def files(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, _file_callback, id_map=id_map)
    
    
def _search_callback(key, person, user_type, id_map={}):
    # The search query
    
    q = id_map['q']

    search_queue = libsearch.parse_query(q)
    
    if 'g' in id_map:
        groups = id_map['g']
    else:
        groups = []
    
    tag = Tag.objects.get(name=id_map['tag'])
    
    #samples = Sample.objects.filter(tagsamplesearch__tag_keyword_search__keyword__name__contains=q).filter(tagsamplesearch__tag_keyword_search__tag__id=tag.id).distinct()
    
    samples = _search_samples(tag, groups, search_queue)
    
    if 'type' in id_map:
        samples = samples.filter(expression_type_id__in=id_map['type'])
    
    if 'person' in id_map:
        samples = samples.filter(persons__in=id_map['person'])
    
    # filter by size
    
    max_count = id_map['max_count']
    
    if len(search_queue) == 0 or len(groups) == 0:
        # Blanket search so just return the first n records
        samples = samples[:max_count]
    
    serializer = SampleSerializer(samples, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)


def _search_samples(tag, groups, search_queue):
    if len(search_queue) == 0:
        if len(groups) > 0:
            return Sample.objects.filter(groups__in=groups).distinct().order_by('name')
        else:
            # If there is no query, default to return 100 results ordered 
            # by name
            return Sample.objects.order_by('name')

    stack = libcollections.Stack()

    for e in search_queue:
        if e.op == 'MATCH':
            if len(groups) > 0:
                samples = Sample.objects.filter(tagsamplesearch__tag_keyword_search__keyword__name__contains=e.text) \
                    .filter(tagsamplesearch__tag_keyword_search__tag__id=tag.id) \
                    .filter(groups__in=groups) \
                    .distinct().order_by('name')
            else:
                samples = Sample.objects.filter(tagsamplesearch__tag_keyword_search__keyword__name__contains=e.text) \
                    .filter(tagsamplesearch__tag_keyword_search__tag__id=tag.id) \
                    .distinct().order_by('name')
    
            stack.push(samples)
        elif e.op == 'AND':
            stack.push(stack.pop().intersection(stack.pop())) #(tempStack.pop(), tempStack.pop()));
        elif e.op == 'OR':
            stack.push(stack.pop().union(stack.pop()))
        else:
            pass

    return stack.pop()


def search(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('q', '') \
        .add('tag', '/All') \
        .add('type', arg_type=str, multiple=True) \
        .add('person', None, int, multiple=True) \
        .add('g', None, arg_type=str, multiple=True) \
        .add('max_count', 100) \
        .parse(request)
    
    print(id_map)
    
    return auth.auth(request, _search_callback, id_map=id_map)
    
