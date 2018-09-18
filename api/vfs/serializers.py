from rest_framework import serializers
from api.vfs.models import VFSFile

class VFSFileSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    pid = serializers.IntegerField(source='parent_id')
    t = serializers.IntegerField(source='type_id')
    d = serializers.DateTimeField('%Y-%m-%d', source='created')
    
    class Meta:
        model = VFSFile
        fields = ('id', 'pid', 'n', 'path', 't', 'd')
