from rest_framework import serializers
from api.genomic.elements.models import Element

class ElementSerializer(serializers.ModelSerializer):
    """
    Serialize sample to JSON
    """
    
    #id = serializers.IntegerField()

    class Meta:
        model = Element
        fields = ('id', 'name')
        
