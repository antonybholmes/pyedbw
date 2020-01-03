from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import base64

def about(request):
    return JsonResponse({"name":"edbw","version":"10.0","copyright":"Copyright (C) 2014-2019 Antony Holmes"}, safe=False)

def json_page_resp(name, page, paginator):
    """
    Returns a standardized page response
    """
    
    page_rows = paginator.get_page(page)
    
    return JsonResponse({'page':page, 'pages':paginator.num_pages, name:[x['json'] for x in page_rows], 'size':len(page_rows)}, safe=False)


def json_resp(rows):
    """
    For rows containing a json field.
    """
    
    return JsonResponse([x['json'] for x in rows], safe=False)



def test(request):
    print(request.META)
    print(base64.b64decode(request.headers['Authorization'][6:]))
    print(base64.b64decode(request.headers['Authorization'].split(' ')[1]).decode('utf-8').split(':'))
    return JsonResponse(request.headers, safe=False)
