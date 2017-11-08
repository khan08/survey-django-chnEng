from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Instrument,Interview,Participant,Answer
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from . import models, forms
from django.core import serializers

# Create your views here.

class InterviewIndexView(generic.ListView):
    context_object_name = 'interview'
    template_name = "interview.html"
    def get_queryset(self):
        interview = Interview.objects.get(id=self.kwargs['pk'])
        participant = Participant.objects.get(id=self.kwargs['participant_id'])
        return {'instruments':interview.instrument.all(),'name':interview.name,'participant':participant}

class HomeView(generic.ListView):
    context_object_name = 'assignments'
    template_name = "home.html"
    def get_queryset(self):
        assignments = models.Assignment.objects.all()
        return assignments

def prepare_blank_answers(interview,instrument, user, participant):
    for question in instrument.question_set.all():
        answer = models.Answer(interview=interview,instrument=instrument,question=question,user=user,participant=participant)
        answer.save()

def questionView(request, instrument_id, interview_id, participant_id):
    instrument = get_object_or_404(models.Instrument, id=instrument_id)
    interview = get_object_or_404(models.Interview, id=interview_id)
    user = request.user
    participant = get_object_or_404(models.Participant, id=participant_id)
    answers = Answer.objects.filter(interview=interview,instrument=instrument,user=user,participant=participant)
    if len(instrument.answer_set.all()) == 0:
        prepare_blank_answers(interview,instrument,user,participant)
    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, queryset=answers)
        if formset.is_valid():
            formset.save()
            for form in formset:
                print(form)
            return HttpResponse("Success.")
        else:
            print(formset.errors)
            print(request.POST)
    else:
        formset = forms.AnswerFormSet(queryset=answers)

    questions = serializers.serialize("json", instrument.question_set.all())
    return render_to_response('instrument.html',
                              {'formset': formset, 'questions': questions})


