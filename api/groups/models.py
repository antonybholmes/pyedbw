from django.db import models
from datetime import datetime 
from django.contrib.postgres.fields import JSONField     

from api.models import User


class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    created = models.DateTimeField()
    json = JSONField()

    class Meta:
        db_table = 'group'
        
#class UserGroup(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    group = models.ForeignKey(Group, on_delete=models.CASCADE)
#    created = models.DateTimeField()
#
#    class Meta:
#        db_table = 'user_group'



#class GroupJson(models.Model):
#    json = JSONField()
#
#    class Meta:
#        db_table = 'groups'
#        
