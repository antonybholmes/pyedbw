from rest_framework import serializers
from api.experiments.models import Experiment

class ExperimentSerializer(serializers.ModelSerializer):
    n = serializers.CharField(source='name')
    ds = serializers.CharField(source='description')
    d = serializers.DateTimeField('%Y-%m-%d', source='created')

    class Meta:
        model = Experiment
        fields = ('id', 'n', 'ds', 'd')
