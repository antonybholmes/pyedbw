from django.db import models
from datetime import datetime
from api.samples.models import Sample

class ElementType(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'genomic_elements_types'

                
class Element(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    type = models.ForeignKey(ElementType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)

    class Meta:
        db_table = 'genomic_elements'
