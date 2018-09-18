from django.db import models
from datetime import datetime

class Experiment(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created = models.DateTimeField('%Y-%m-%d')

    class Meta:
        db_table = 'experiments'

