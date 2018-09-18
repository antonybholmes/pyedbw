from api.persons.models import Person
from django.http import JsonResponse

EMPTY_JSON_LIST = JsonResponse([], safe=False)

def empty_list_callback():
    """
    Default error function
    """
    return EMPTY_JSON_LIST


def auth(request, callback, error_callback=empty_list_callback, id_map=None, check_for=None, pkey_only=True):
    """
    Checks an api key in the database matches a person and if so
    runs callback, otherwise returns an error response.
    
    Parameters
    ----------
    key : str
        API key
    callback : function
        Function to call if key is valid.
    error_callback : function, optional
        Function to call if key is invalid. Defaults to returning
        an empty json list.
    pkey_only : bool, optional
        If set to True (default) will ignore id params that are less
        than 1 since these are not valid database ids
    
    Returns
    -------
    str
        JSON string of results
    """
    
    if 'key' not in request.GET:
        return error_callback()
    
    key = request.GET['key']
    
    if isinstance(check_for, set):
        for id in check_for:
            if id not in id_map:
                print(id, 'not found in check_for')
                return error_callback()
     
    for n in id_map:
        for id in id_map[n]:
            # test all int ids for being valid, ignore strings etc
            if pkey_only and isinstance(id, int) and id < 1:
                #print(id, 'is invalid int')
                return error_callback()
 
    
    persons = Person.objects.filter(api_key=key)
    person = persons[0]
    
    user_type = get_user_type(person)
    
    if len(persons) > 0:
        # If there is a person send it to the callback
        return callback(key, persons[0], user_type, id_map=id_map)
    else:
        # return an empty response otherwise
        #print('invalid person')
        return error_callback()


def parse_ids(request, *args, **kwargs):
    """
    Parse ids out of the request object and convert to ints and add
    as a named list to the id_map.
    
    Parameters
    ----------
    request : request
        URL request
    *args
        List of strings of id names to parse
    **kwargs
        If a map parameter named 'id_map' is passed through kwargs,
        it will have the ids loaded into it. In this way existing
        maps can be used/reused with this method rather than creating
        a new map each time.
        
    Returns
    -------
    dict
        dictionary of named ids where each entry is a list of numerical
        ids. This is to allow for multiple parameters with the same
        name.
    """
    
    if 'id_map' in kwargs:
        id_map = kwargs['id_map']
    else:
        id_map = {}
        
    for p in args:
        if isinstance(p, dict):
            n = next(iter(p))
        else:
            n = p
            
        if n in request.GET:
            # if the sample id is present, pass it along
            ids = param_str_to_int(request, n)
            
            if len(ids) > 0:
                # Only add non empty lists to dict
                id_map[n] = ids
        else:
            if isinstance(p, dict):
                id_map[n] = [p[n]]
            
    return id_map
    

def parse_params(request, *args, **kwargs):
    """
    Parse ids out of the request object and convert to ints and add
    as a named list to the id_map.
    
    Parameters
    ----------
    request : request
        URL request
    *args
        List of strings of id names to parse
    **kwargs
        If a map parameter named 'id_map' is passed through kwargs,
        it will have the ids loaded into it. In this way existing
        maps can be used/reused with this method rather than creating
        a new map each time.
        
    Returns
    -------
    dict
        dictionary of named ids where each entry is a list of numerical
        ids. This is to allow for multiple parameters with the same
        name.
    """
    
    if 'id_map' in kwargs:
        id_map = kwargs['id_map']
    else:
        id_map = {}
    
    for p in args:
        if isinstance(p, dict):
            n = next(iter(p))
        else:
            n = p
            
        if n in request.GET:
            # if the sample id is present, pass it along
            ids = request.GET.getlist(n)
            
            if len(ids) > 0:
                # Only add non empty lists to dict
                id_map[n] = ids
        else:
            # If arg does not exist, supply a default
            if isinstance(p, dict):
                id_map[n] = [p[n]]
            
    return id_map
    
    
def param_str_to_int(request, name):
    """
    Converts multiple url parameters with the same name to a list of
    ints.
    
    Parameters
    ----------
    request : request
        URL request
    name : str
        URL parameter name
        
    Returns
    -------
    list
        int list of parameter values.
    
    """
    
    return [int(x) for x in request.GET.getlist(name) if x.isdigit()]


def get_user_type(person):
    """
    Determine the user type which can either be 'Superuser',
    'Administator', or 'Normal' in order of status. Most users should
    be 'Normal'
    
    Parameters
    ----------
    person : Person
        Person record
    
    Returns
    -------
    str
        A string representing the user type.
    """
    
    s = Person.objects.filter(id=person.id, groups__name='Superuser').exists()
    
    if s:
        return 'Superuser'
    
    s = Person.objects.filter(id=person.id, groups__name='Administrator').exists()
    
    if s:
        return 'Administrator'
    
    return 'Normal'
