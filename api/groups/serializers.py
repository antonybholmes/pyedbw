from rest_framework import serializers
from django.contrib.auth.models import Group

class GroupSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    #c = serializers.CharField(source='color')

    class Meta:
        model = Group
        fields = ('id', 'n')
