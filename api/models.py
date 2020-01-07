from django.db import models
from datetime import datetime 
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField  

from login.models import User

class APIKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'api_key'

#class UserAPIKey(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)    
#    api_key = models.ForeignKey(APIKey, on_delete=models.CASCADE)
#
#    class Meta:
#        db_table = 'api_user_keys'

class Tag(models.Model):
    name = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tags'
        
        
class TagType(models.Model):
    name = models.CharField(max_length=255)
    #created = models.DateTimeField()

    class Meta:
        db_table = 'tag_types'
        
        

