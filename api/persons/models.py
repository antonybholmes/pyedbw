from django.db import models
from datetime import datetime
from api.groups.models import Group
from django.contrib.postgres.fields import JSONField     


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    groups = models.ManyToManyField(Group, through='GroupPerson')
    api_key = models.CharField(max_length=64)
    created = models.DateTimeField()

    @property
    def name(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = 'persons'
        
        
class PersonJson(models.Model):
    json = JSONField()

    class Meta:
        db_table = 'persons'


class GroupPerson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created = models.DateTimeField()

    class Meta:
        db_table = 'groups_persons'
