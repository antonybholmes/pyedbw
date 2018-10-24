from rest_framework import serializers
from api.ucsc.models import Track

class TrackSerializer(serializers.ModelSerializer):
    """
    Serialize sample to JSON
    """
    
    u = serializers.CharField(source='url')
    d = serializers.DateTimeField('%Y-%m-%d', source='created')
    
    class Meta:
        model = Track
        fields = ('u')
        
