from login.models import User
from api.models import APIKey
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
import re
import base64

EMPTY_JSON_LIST = JsonResponse([], safe=False)

INT_REGEX = re.compile(r'^\d+$')
FLOAT_REGEX = re.compile(r'^\d+\.\d+$')
KEY_REGEX = re.compile(r'^[A-Za-z0-9]+$')

AUTH_ERROR_INVALID_ID = JsonResponse({'success': False, 'error':'Invalid Id.'}, 
                                     safe=False)

AUTH_ERROR_MALFORMED_API_KEY = JsonResponse({'success': False, 'error':'Malformed key.'}, 
                                            safe=False)

AUTH_ERROR_INVALID_API_KEY = JsonResponse({'success': False, 'error':'Invalid key.'}, 
                                          safe=False)

def auth(request, 
         callback, 
         id_map=None, 
         check_for=None, 
         pkey_only=True):
    """
    Checks an api key in the database matches a person and if so
    runs callback, otherwise returns an error response.
    
    Parameters
    ----------
    key : str
        API key
    callback : function
        Function to call if key is valid.
    pkey_only : bool, optional
        If set to True (default) will ignore id params that are less
        than 1 since these are not valid database ids
    
    Returns
    -------
    str
        JSON string of results
    """
    
    key = None
    
    if 'Authorization' in request.headers:
        # Priortize getting api key from header using http basic auth
        
        # decode key from auth request. First element is type e.g. basic
        # and second element is base64 encoded key
        _, value = request.headers['Authorization'].split(' ')
        key, _ = base64.b64decode(value).decode('utf-8').split(':')
    else:
        # Attempt to get key from URL
        key = request.GET.get('key', None)
        
    if key is None or not KEY_REGEX.match(key):
        return AUTH_ERROR_MALFORMED_API_KEY
 
    if isinstance(check_for, set):
        for id in check_for:
            if id not in id_map:
                return AUTH_ERROR_INVALID_ID
    
    for name, values in id_map.items():
        if isinstance(values, list):
            for id in values:
                # test all int ids for being valid, ignore strings etc
                if pkey_only and isinstance(id, int) and id < 1:
                    return AUTH_ERROR_INVALID_ID
        elif isinstance(values, int):
            id = values
            if pkey_only and isinstance(id, int) and id < 1:
                return AUTH_ERROR_INVALID_ID
        else:
            pass
 
    apikeys = APIKey.objects.filter(key=key)
    
    if len(apikeys) == 0:
        return AUTH_ERROR_INVALID_API_KEY
    
    user = apikeys[0].user
    user_type = get_user_type(user)
    
        # If there is a person send it to the callback
    return callback(key, user, user_type, id_map=id_map)


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
    
def parse_arg(x):
    """
    Parse a string argument and attempt to turn numbers into actual
    number types.
    
    Parameters
    ----------
    x : str
        A string arg.
    
    Returns
    -------
    str, float, or int
        x type converted.
    """
    
    if x.replace('.', '').isdigit():
        if x.isdigit():
            x = int(x)
        else:
            x = float(x)
                
    return x

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
            # If p is a dict then assume the value is the default value
            # and the name is the key. Furthermore assume dict only
            # contains one entry
            name = next(iter(p))
        elif isinstance(p, tuple):
            # If p is a dict then assume the value is the default value
            # and the name is the key. Furthermore assume dict only
            # contains one entry
            name = p[0]
        elif isinstance(p, str):
            name = p
        else:
            # arg seems invalid so skip it
            continue
        
        print(request.GET)
        
        if name in request.GET:
            # if the sample id is present, pass it along
            values = [parse_arg(x) for x in request.GET.getlist(name)]
            
            if len(values) > 0:
                # Only add non empty lists to dict
                id_map[name] = values
        else:
            # If arg does not exist, supply a default
            if isinstance(p, dict):
                # values of args are returned as a list even if there
                # is only one arg
                id_map[name] = [p[name]]
            elif isinstance(p, tuple):
                id_map[name] = [p[1]]
            else:
                pass
            
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


def get_user_type(user):
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

    if user.is_superuser:
        return 'Superuser'
    elif user.is_staff:
        return 'Administrator'
    else:
        return 'Normal'
