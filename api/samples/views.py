import sys
import collections

from django.core.cache import cache
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.core.paginator import Paginator
from api.models import Tag
from api.persons.models import Person
from login.serializers import UserSerializer
from api.vfs.models import VFSFile
from api.vfs.serializers import VFSFileSerializer
from api.samples.models import Sample, Set, TagSampleSearch, TagKeywordSearch, SampleFile, SampleTag #, SampleIntTag, SampleFloatTag
from api.samples.serializers import SampleSerializer, SetSerializer #, SampleTagSerializer
from api import auth, libsearch, libcollections, views
from edbw import settings
from login.models import User

import libhttp
import collections

def _get_page_response(serializer, page=0, paginator=None):
    if page > 0:
        return JsonResponse({'page':page, 'pages':paginator.num_pages, 'results':serializer.data}, safe=False)
    else:
        # The old style of response which is just a list of results
        return JsonResponse(serializer.data, safe=False)
  
def _sample_callback(key, user, user_type, id_map={}):
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = 1
    
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
    
    if 'sample' in id_map:
        ids = id_map['sample']
        
        if user_type != 'Normal':
            rows = Sample.objects.filter(id__in=ids)
        else:
            rows = Sample.objects.filter(groups__user__id=user.id, id__in=ids).distinct()
    else:
        # return all samples
        
        if user_type != 'Normal':
            rows = Sample.objects.all()
        else:
            # Normal users are filtered by the groups they belong to
            rows = Sample.objects.filter(groups__user__id=user.id)
    
    rows = rows.order_by('name')
    
    paginator = Paginator(rows, records)
    
    page_rows = paginator.get_page(page)
    
    serializer = SampleSerializer(page_rows, many=True, read_only=True)
    
    data = _get_page_response(serializer, 
                              page=page if 'page' in id_map else 0, 
                              paginator=paginator)
    
    return data


def samples(request):
    print('samples')
 
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('sample', None, int, multiple=True) \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .parse(request)
        
    #id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, _sample_callback, id_map=id_map)


def _users_callback(key, user, user_type, id_map={}):
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = 1
    
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
    
    rows = User.objects.filter(sampleperson__sample__in=id_map['sample'])
    
    paginator = Paginator(rows, records)
    
    page_rows = paginator.get_page(page)
    
    serializer = UserSerializer(page_rows, many=True, read_only=True)
    
    data = _get_page_response(serializer, 
                              page=page if 'page' in id_map else 0, 
                              paginator=paginator)
    
    return data


def users(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('sample', None, int, multiple=True) \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .parse(request)
    
    return auth.auth(request, _users_callback, id_map=id_map, check_for={'sample'})

def persons(request):
    return users(request)
    
    
def _sets_callback(key, user, user_type, id_map={}):
    if 'set' in id_map:
        sets = id_map['set']
        
        samples = Sample.objects.filter(sets__in=sets).distinct().order_by('name')
        
        serializer = SampleSerializer(samples, many=True, read_only=True)
    
        return JsonResponse(serializer.data, safe=False)
    else:
        serializer = SetSerializer(Set.objects.all(), many=True, read_only=True)
    
        return JsonResponse(serializer.data, safe=False)    


def sets(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('set', None, int, multiple=True) \
        .parse(request)
    
    return auth.auth(request, _sets_callback, id_map=id_map)
    

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
    
    for tag in tags.values('tags')[0]['tags']:
        print(tag)
        ret += '{}:{}\n'.format(tag['id'], tag['v'])
    
    return ret
    

def _tags_callback(key, user, user_type, id_map={}):
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = -1
    
    sample = id_map['sample']
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
    f = id_map['format']
    
    cache_key = '_'.join(['tags',
        str(sample), 
        str(page),
        str(records),
        f]) # needs to be unique
        
    data = cache.get(cache_key) # returns None if no key-value pair
    
    # shortcut and return cached copy
    if data is None:
        #if f == 'text':
        #    data = HttpResponse(_json_to_str(Sample.objects.filter(id=sample)), content_type='text/plain; charset=utf8')
        #else:
        rows = Sample.objects.filter(id=sample).values('json')
        
        #print(rows)
        
        #paginator = Paginator(rows, records)
    
        #print(tags.values('data')[0]['data'][0]['id'])

        #return JsonResponse(tags.values('tags')[0]['tags'], safe=False)
        
        if page > 0:
            data = JsonResponse({'page':1, 'pages':1, 'tags':rows[0]['json']}, safe=False)
        else:
            data = JsonResponse(rows[0]['json'], safe=False) #views.json_resp(paginator.get_page(1))
                
        cache.set(cache_key, data, settings.CACHE_TIME_S)
        
    return data


def tags(request):
    id_map = libhttp.ArgParser() \
        .add('key') \
        .add('sample', arg_type=int) \
        .add('tag', arg_type=int) \
        .add('format', 'json') \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .parse(request)
    
    return auth.auth(request, _tags_callback, id_map=id_map, check_for={'sample'})
       
    
def geo_callback(key, user, user_type, id_map={}):
    return JsonResponse([], safe=False)    


def geo(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, geo_callback, id_map=id_map)
    

def _file_callback(key, user, user_type, id_map={}):
    files = VFSFile.objects.filter(samplefile__sample__in=id_map['sample'])
    
    serializer = VFSFileSerializer(files, many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)    


def files(request):
    id_map = auth.parse_ids(request, 'sample')
    
    return auth.auth(request, _file_callback, id_map=id_map)
    
    
def _search_callback(key, user, user_type, id_map={}):
    # records per page
    records = min(id_map['records'], settings.MAX_RECORDS_PER_PAGE)
      
    # The search query
    
    q = id_map['q']

    # Groups are used to categorize samples such as by person or type
    # to make filtering easier
    groups = []
    
    if 'g' in id_map:
        groups = id_map['g']
    
    if 'group' in id_map:
        groups = id_map['group']
        
    if 'type' in id_map:
        types = id_map['type']
    else:
        types = []
        
    if 'user' in id_map:
        users = id_map['user']
    else:
        users = []
        
    if 'page' in id_map:
        page = id_map['page']
    else:
        page = -1
    
    if 'set' in id_map:
        sets = id_map['set']
    else:
        sets = []
    
    cache_key = '_'.join(['q',
        q, 
        str(page), 
        str(records),
        ':'.format(groups), 
        ':'.format(types), 
        ':'.format(users),
        ':'.format(sets)]) # needs to be unique
        
    data = cache.get(cache_key) # returns None if no key-value pair
    
    # shortcut and return cached copy
    if data is not None:
        print('Using cache of', cache_key)
        return data
        
    search_queue = libsearch.parse_query(q)
    
    #print('groups', groups)
    
    tag = Tag.objects.get(name=id_map['tag'])
    
    samples = _search_samples(tag, groups, search_queue)
    
    if len(types) > 0:
        samples = samples.filter(expression_type_id__in=types)
    
    if len(users) > 0:
        samples = samples.filter(users__in=users)

    if user_type == 'Normal':
        #print('normal')
         
        # filter what user can see
        samples = samples.filter(groups__user__id=user.id)
    
    if len(sets) > 0:
        set_samples = Sample.objects.filter(sets__in=sets) #.distinct().order_by('name')
        
        if len(search_queue) == 0:
            # If user didn't search for anything, results are just
            # the selected sets
            samples = set_samples
        else:
            # If there was a search, take the union of the sets and
            # the search query
            samples = samples.union(set_samples)
    
    # Sort them
    samples = samples.distinct().order_by('name')
    
    paginator = Paginator(samples, records)
    
    if page > 0:
        page_rows = paginator.get_page(page)
    else:
        page_rows = paginator.get_page(1)
    
    sortby = id_map['sortby']
    
    if sortby != '':
        # Alt name is a shorter version of the tag name that can be
        # passed into a URL
        sample_tags = SampleTag.objects.filter(sample__in=page_rows).filter(tag__alt_name=sortby)
        
        sort_map = collections.defaultdict(list)
        
        for sample_tag in sample_tags:
            sort_map[sample_tag.str_value].append(SampleSerializer(sample_tag.sample, read_only=True).data)
            
        #serializer = SampleSerializer(page_rows, many=True, read_only=True)
        
        data = JsonResponse({'page':page, 
                             'pages':paginator.num_pages, 
                             'data':sort_map}, safe=False)
    else:
        serializer = SampleSerializer(page_rows, many=True, read_only=True)
        
        if page > 0:
            # If we use the page param, return results in the new format
            # that include page and pages meta data
            data = JsonResponse({'page':page, 
                                 'pages':paginator.num_pages, 
                                 'results':serializer.data, 
                                 'size':len(page_rows)}, safe=False)
        else:
            # The old style of response which is just a list of results
            data = JsonResponse(serializer.data, safe=False)
            
    cache.set(cache_key, data, settings.CACHE_TIME_S)
        
    return data


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
        .add('user', None, int, multiple=True) \
        .add('g', None, int, multiple=True) \
        .add('group', None, int, multiple=True) \
        .add('set', None, int, multiple=True) \
        .add('page', arg_type=int) \
        .add('records', default_value=settings.DEFAULT_RECORDS) \
        .add('sortby', '') \
        .parse(request)
     
    #print(id_map)
    
    return auth.auth(request, _search_callback, id_map=id_map)
    
