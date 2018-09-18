from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from api.models import Tag
from api.types.models import Organism, Genome, Role, DataType
from api.types.serializers import OrganismSerializer, TagSerializer, GenomeSerializer, DataTypeSerializer, RoleSerializer


def organisms(request):
    """
    Display all organisms
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    serializer = OrganismSerializer(Organism.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    
    
def tags(request):
    """
    Display all tags
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    serializer = TagSerializer(Tag.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    

def genomes(request):
    """
    Display all genomes
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    serializer = GenomeSerializer(Genome.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
    
    
def roles(request):
    """
    Display all tags
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    serializer = RoleSerializer(Role.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)


def data(request):
    """
    Display all genomes
    
    Parameters
    ----------
    request : WSGIRequest
        URL request parameters
    """
    
    serializer = DataTypeSerializer(DataType.objects.all(), many=True, read_only=True)
    
    return JsonResponse(serializer.data, safe=False)
