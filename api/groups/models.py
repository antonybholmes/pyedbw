from django.db import models
from datetime import datetime 
     

class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'groups'
        
