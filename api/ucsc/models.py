from django.db import models
from datetime import datetime
from api.samples.models import Sample

class TrackType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'ucsc_track_types'

class Track(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    track_type = models.ForeignKey(TrackType, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

    class Meta:
        db_table = 'ucsc_tracks'
