from django.views import generic
from .models import Interview,Participant,Answer,Instrument
from django import forms
from django.shortcuts import render_to_response, get_object_or_404,redirect
from . import models, forms
from django.core import serializers

# Create your views here.

class InterviewIndexView(generic.ListView):
    context_object_name = 'interview'
    template_name = "interview.html"
    def get_queryset(self):
        interview = Interview.objects.get(id=self.kwargs['pk'])
        participant = Participant.objects.get(id=self.kwargs['participant_id'])
        assignment = models.Assignment.objects.get(interview=interview,participant=participant)
        interviewInstance,created = models.InterviewInstance.objects.get_or_create(assignment=assignment)
        return {'instruments':interview.instrument.all(),'interviewInstance':interviewInstance}

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
    answers = Answer.objects.filter(interview=interview,instrument=instrument,participant=participant)
    if len(answers) == 0:
        prepare_blank_answers(interview,instrument,user,participant)
        answers = Answer.objects.filter(interview=interview, instrument=instrument,participant=participant)
    if request.method == 'POST':
        formset = forms.AnswerFormSet(request.POST, queryset=answers.order_by('question__sort_value'),initial=[{'user':request.user}])
        if formset.is_valid():
            formset.save()
            if 'Next' in request.POST:
                try:
                    instrumentInstance = Interview.instrument.through.objects.get(instrument=instrument,interview=interview)
                    next_instrument = Interview.instrument.through.objects.get(interview=interview,sort_value=instrumentInstance.sort_value+1)
                    next_id = next_instrument.instrument.id
                    return redirect("instrument",interview_id=interview_id,instrument_id=next_id,participant_id=participant_id)
                except Exception:
                    pass
            if 'Prev' in request.POST:
                try:
                    instrumentInstance = Interview.instrument.through.objects.get(instrument=instrument,interview=interview)
                    next_instrument = Interview.instrument.through.objects.get(interview=interview,sort_value=instrumentInstance.sort_value-1)
                    next_id = next_instrument.instrument.id
                    return redirect("instrument",interview_id=interview_id,instrument_id=next_id,participant_id=participant_id)
                except Exception:
                    pass
        if 'Save' in request.POST:
                return redirect("interview",pk=interview_id,participant_id=participant_id)
        else:
            print(formset.errors)
            print(request.POST)
    else:
        print(answers)
        formset = forms.AnswerFormSet(queryset=answers.order_by('question__sort_value'))

    questions = serializers.serialize("json", instrument.question_set.all())
    return render_to_response('instrument.html',
                              {'formset': formset, 'questions': questions, 'instrument':instrument, 'interview':interview})




