from django.db import models
from datetime import datetime 
from django.contrib.postgres.fields import JSONField     

class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'groups'
        

class GroupJson(models.Model):
    json = JSONField()

    class Meta:
        db_table = 'groups'
        
