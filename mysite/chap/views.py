from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import generic
from .models import Instrument,Interview
from django import forms
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from . import models, forms

# Create your views here.

class InterviewIndexView(generic.ListView):
    context_object_name = 'interview'
    template_name = "interview.html"
    def get_queryset(self):
        interview = Interview.objects.get(id=self.kwargs['pk'])
        return interview.instrument.all()

def prepare_blank_answers(interview,instrument,request):
    for question in instrument.question_set.all():
        answer = models.Answer(interview=interview,instrument=instrument,question=question)#,user=request.user)
        answer.save()

def questionView(request, instrument_id, interview_id):
    instrument = get_object_or_404(models.Instrument, id=instrument_id)
    interview = get_object_or_404(models.Interview, id=interview_id)
    if len(instrument.answer_set.all()) == 0:
        prepare_blank_answers(interview,instrument,request)
    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, instance=instrument)
        if formset.is_valid():
            formset.save()
            for form in formset:
                print(form)
            return HttpResponse("Success.")
    else:
        formset = forms.AnswerFormSet(instance=instrument)
    return render_to_response('instrument.html',
                              {'formset': formset, 'instrument': instrument})
