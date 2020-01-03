from django.db import models
from datetime import datetime 
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField  

from api.groups.models import Group

class User(AbstractUser):
    affiliation = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=255, default='')
    address = models.CharField(max_length=255, default='')
    #groups = models.ManyToManyField(Group, through='UserGroup')
    json = JSONField(default=list)

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created = models.DateTimeField()

class Key(models.Model):
    name = models.CharField(max_length=255)

class Tag(models.Model):
    name = models.CharField(max_length=255)
    alt_name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'tags'
        
        
class TagType(models.Model):
    name = models.CharField(max_length=255)
    #created = models.DateTimeField()

    class Meta:
        db_table = 'tag_types'
        
        

