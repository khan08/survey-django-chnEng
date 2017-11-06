# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
import datetime
from sortedm2m.fields import SortedManyToManyField
from django.contrib.auth.models import User

class Instrument(models.Model):
    abbr = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)
    chinesename = models.CharField(db_column='chineseName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    chinesecontent = models.CharField(db_column='chineseContent', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    tran_date = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'instrument'

class Interview(models.Model):
    instrument = SortedManyToManyField(Instrument)
    name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    tran_date = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    #tran_user = models.CharField(max_length=15, blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        db_table = 'interview'



class Question(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    ch_content = models.CharField(max_length=1000, blank=True, null=True)
    help = models.CharField(max_length=800, blank=True, null=True)
    ch_help = models.CharField(max_length=1000, blank=True, null=True)
    hascomment = models.IntegerField(db_column='hasComment', blank=True, null=True)  # Field name made lowercase.
    label = models.CharField(max_length=20, blank=True, null=True)
    tran_date = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    sort_value = models.IntegerField(default=0)


    def __str__(self):
        return self.content

    class Meta:
        db_table = 'question'
        ordering = ('sort_value',)

class Choice(models.Model):
    question = models.ForeignKey(Question)
    content = models.CharField(max_length=200, blank=True, null=True)
    chcontent = models.CharField(db_column='chContent', max_length=200, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(max_length=5, blank=True, null=True)
    triggersub = models.IntegerField(blank=True, null=True)
    tran_date = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)
    sort_value = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'choice'
        ordering = ('sort_value',)

class Answer(models.Model):
    #user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    #participant = models.ForeignKey(User, related_name='participant')

    instrument = models.ForeignKey(Instrument)
    interview = models.ForeignKey(Interview)
    class Meta:
        db_table = 'answer'