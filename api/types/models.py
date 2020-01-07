from django.db import models
from datetime import datetime 
     

class Organism(models.Model):
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'organisms'
        
        
class Role(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'role'
        
        
class Genome(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'genomes'
        

class DataType(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'data_types'
