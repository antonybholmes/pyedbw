from django.db import models
from datetime import datetime
from api.experiments.models import Experiment
from api.models import Tag, TagType
from api.persons.models import Person, GroupPerson
from api.vfs.models import VFSFile
from api.groups.models import Group
from django.contrib.postgres.fields import JSONField

class Set(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'sets'
        
        
class Sample(models.Model):
    experiment_id = models.IntegerField()
    #experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # We need this to link samples to groups so we can subsequently
    # link persons to groups and transitively, samples to persons via
    # the shared groups they belong to.
    groups = models.ManyToManyField(Group, through='GroupSample')
    persons = models.ManyToManyField(Person, through='SamplePerson')
    sets = models.ManyToManyField(Set, through='SetSample')
    organism_id = models.IntegerField()
    expression_type_id = models.IntegerField()
    # tags = models.TextField()
    created = models.DateTimeField('%Y-%m-%d')

    class Meta:
        db_table = 'samples'

class SampleTag(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_type = models.ForeignKey(TagType, on_delete=models.CASCADE)
    str_value = models.CharField(max_length=255)
    int_value = models.IntegerField()
    float_value = models.FloatField()
    created = models.DateTimeField()
    json = JSONField()
    
    class Meta:
        db_table = 'sample_tags'
                
#class SampleTagsJson(models.Model):
    #sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    #data = models.TextField()

    #class Meta:
        #db_table = 'sample_tags_json'
 
#class SampleTagJson(models.Model):
#    """
#    A view onto the samples table that exposes the JSON representation
#    of the samples.
#    """
#    json = JSONField()
# 
#    class Meta:
#        db_table = 'samples'
        
        
class SetSample(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sets_samples'
        
        
class GroupSample(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    created = models.DateTimeField()

    class Meta:
        db_table = 'groups_samples'
        
        
class SampleFile(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    vfs = models.ForeignKey(VFSFile, on_delete=models.CASCADE)

    class Meta:
        db_table = 'sample_files'
        
        
class SamplePerson(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    created = models.DateTimeField()

    class Meta:
        db_table = 'sample_persons'
        
        
#class SampleTag(models.Model):
    #sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    #tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #value = models.CharField(max_length=255)
    #created = models.DateTimeField()
    
    #class Meta:
        #db_table = 'tags_sample'

        
#class SampleIntTag(models.Model):
    #sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    #tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #value = models.IntegerField()
    #created = models.DateTimeField()
    
    #class Meta:
        #db_table = 'tags_sample_int'
        

#class SampleFloatTag(models.Model):
    #sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    #tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #value = models.FloatField()
    #created = models.DateTimeField()
    
    #class Meta:
        #db_table = 'tags_sample_float'
        

class Keyword(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField()

    class Meta:
        db_table = 'keywords'
        
        
class TagKeywordSearch(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    
    created = models.DateTimeField()

    class Meta:
        db_table = 'tags_keywords_search'
        
        
class TagSampleSearch(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    tag_keyword_search = models.ForeignKey(TagKeywordSearch, on_delete=models.CASCADE)
    created = models.DateTimeField()

    class Meta:
        db_table = 'tags_samples_search'
        

