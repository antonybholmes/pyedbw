from rest_framework import serializers
from api.models import Tag
from api.types.models import Organism, Genome, Role, DataType

class OrganismSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    sn = serializers.CharField(source='scientific_name')
    
    class Meta:
        model = Organism
        fields = ('id', 'n', 'sn')
        
        
class TagSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    
    class Meta:
        model = Tag
        fields = ('id', 'n')
        

class RoleSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    
    class Meta:
        model = Role
        fields = ('id', 'n')


class GenomeSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    
    class Meta:
        model = Genome
        fields = ('id', 'n')


class DataTypeSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    
    class Meta:
        model = DataType
        fields = ('id', 'n')
