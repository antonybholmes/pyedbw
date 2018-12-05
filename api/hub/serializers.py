from rest_framework import serializers
from api.ucsc.models import Track

class TrackSerializer(serializers.ModelSerializer):
    """
    Serialize sample to JSON
    """
    
    #id = serializers.IntegerField()
    t = serializers.CharField(source='track_type.name')
    url = serializers.CharField()

    class Meta:
        model = Track
        fields = ('t', 'url',)
        
