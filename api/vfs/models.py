from django.db import models
from datetime import datetime 
     

class VFSFile(models.Model):
    parent_id = models.IntegerField()
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    type_id = models.IntegerField()
    created = models.DateTimeField()

    class Meta:
        db_table = 'vfs'
        
        
