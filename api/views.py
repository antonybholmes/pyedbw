from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

def about(request):
    return JsonResponse({"name":"edbw","version":"9.0","copyright":"Copyright (C) 2014-2018 Antony Holmes"}, safe=False)
