from django.db import models
from datetime import datetime 

        

class Tag(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'tags'
        
        

