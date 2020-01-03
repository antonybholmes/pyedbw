from django.db import models
from datetime import datetime 
from django.contrib.postgres.fields import JSONField        

class VFSFile(models.Model):
    parent_id = models.IntegerField()
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    type_id = models.IntegerField()
    created = models.DateTimeField()
    json = JSONField()

    class Meta:
        db_table = 'vfs'
        
        
#class VFSFileJson(models.Model):
#    # field required for filtering by parent (i.e. listing the
#    # contents of a folder).
#    parent_id = models.IntegerField()
#    
#    json = JSONField()
#
#    class Meta:
#        db_table = 'vfs'
        
        
