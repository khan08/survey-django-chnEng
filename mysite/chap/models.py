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
from address.models import AddressField
from django_mysql.models import JSONField



class Instrument(models.Model):
    abbr = models.CharField(max_length=20)
    name = models.CharField(max_length=100, blank=True, null=True)
    chinesename = models.CharField(db_column='chineseName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    category = models.CharField(max_length=100, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True, null=True)
    chinesecontent = models.CharField(db_column='chineseContent', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'instrument'

class InterviewInstrument(object):
    pass

class Interview(models.Model):
    instrument = SortedManyToManyField(Instrument,base_class=InterviewInstrument)
    name = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=500, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    sort_value = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'choice'
        ordering = ('sort_value',)

class Language(models.Model):
    name = models.CharField(max_length=255)

class Participant(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    chineseName = models.CharField(max_length=255)
    homePhone = models.CharField(max_length=255,blank=True, null=True)
    workPhone = models.CharField(max_length=255,blank=True, null=True)
    cellPhone = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=255,blank=True, null=True)
    address = AddressField(blank=True, null=True)
    speakPre = models.ForeignKey(Language,related_name="speakPre",blank=True, null=True)
    writePre = models.ForeignKey(Language,related_name="writePre",blank=True, null=True)
    readPre = models.ForeignKey(Language,related_name="readPre",blank=True, null=True)
    speakCan = models.ManyToManyField(Language,related_name="speakCan", blank=True, null=True)
    writeCan = models.ManyToManyField(Language,related_name="writeCan", blank=True, null=True)
    readCan = models.ManyToManyField(Language,related_name="readCan", blank=True, null=True)
    family = models.ManyToManyField("self", blank=True, null=True)
    status = models.CharField(max_length=255,blank=True, null=True)
    attr = JSONField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.firstName+" "+self.lastName

class Answer(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    answer = models.CharField(max_length=255)
    participant = models.ForeignKey(Participant)
    instrument = models.ForeignKey(Instrument)
    interview = models.ForeignKey(Interview)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        db_table = 'answer'

class Assignment(models.Model):
    interview = models.ForeignKey(Interview)
    user = models.ForeignKey(User)
    participant = models.ForeignKey(Participant)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    isVerify = models.BooleanField(default=False)
    def __str__(self):
        return self.interview.__str__()+", "+self.user.__str__()+", "+self.participant.__str__()
    class Meta:
        unique_together = (("interview", "user", "participant"),)

class ContactLog(models.Model):
    interview = models.ForeignKey(Interview)
    user = models.ForeignKey(User)
    participant = models.ForeignKey(Participant)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    result = models.CharField(max_length=255)
    attr = JSONField()

class QuestionType(models.Model):
    name = models.CharField(max_length=50)

class InterviewInstance(models.Model):
    interview = models.ForeignKey(Interview)
    participant = models.ForeignKey(Participant)
    percentage = models.FloatField(default=0)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    attr = JSONField()

class InstrumentInstance(models.Model):
    interviewInstance = models.ForeignKey(InterviewInstance)
    instrument = models.ForeignKey(Instrument)
    state = models.IntegerField(blank=True, null=True)
    answered = models.IntegerField(blank=True, null=True)
    total = models.IntegerField(blank=True, null=True)