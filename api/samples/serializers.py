from rest_framework import serializers
from api.samples.models import Sample, Set #, SampleTag, SampleIntTag

class SampleSerializer(serializers.ModelSerializer):
    """
    Serialize sample to JSON
    """
    
    e = serializers.IntegerField(source='experiment_id')
    n = serializers.CharField(source='name')
    o = serializers.IntegerField(source='organism_id')
    t = serializers.IntegerField(source='expression_type_id')
    #persons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    d = serializers.DateTimeField('%Y-%m-%d', source='created')
    
    class Meta:
        model = Sample
        fields = ('id', 'e', 'n', 'o', 't', 'd')
              
class SetSerializer(serializers.ModelSerializer):
    """
    Serialize sample to JSON
    """
    
    
    n = serializers.CharField(source='name')
    
    class Meta:
        model = Set
        fields = ('id', 'n')
        
#class SampleTagSerializer(serializers.ModelSerializer):
    #"""
    #Serialize sample to JSON
    #"""
    
    #id = serializers.CharField(source='tag.id')
    #v = serializers.CharField(source='value')
    
    #class Meta:
        #model = SampleTag
        #fields = ('id', 'v')
        
        
#class SampleIntTagSerializer(serializers.ModelSerializer):
    #"""
    #Serialize sample to JSON
    #"""
    
    #id = serializers.CharField(source='tag.id')
    #v = serializers.CharField(source='value')
    
    #class Meta:
        #model = SampleIntTag
        #fields = ('id', 'v')
