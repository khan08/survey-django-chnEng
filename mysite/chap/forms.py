from django.forms.models import modelformset_factory
from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios,InlineCheckboxes
from crispy_forms.layout import Layout, Field, Div

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = models.Participant
        exclude = {'attr'}

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        question = self.instance.question
        self.choices = question.choice_set.all().order_by('sort_value')
        choice_tup = ((x.id, x) for x in self.choices)
        self.helper = FormHelper()
        self.helper.error_text_inline = False
        self.helper.help_text_inline = True
        self.helper.form_tag = False
        #custom layout
        if question.type==0:
            self.fields['answer'] = forms.ChoiceField(choices=(choice_tup), widget=forms.RadioSelect(), label=question,required=False,help_text=question.help)
            field = InlineRadios('answer',wrapper_class='radio-form',required=False)
        elif question.type==1:
            self.fields['answer'] = forms.MultipleChoiceField(choices=(choice_tup), label=question,required=False)
            field = InlineCheckboxes('answer', choices=choice_tup, wrapper_class='radio-form')
        elif question.type==2:
            self.fields['answer'] = forms.CharField(label=question,required=False)
            field = Field('answer')
        isHide = question.parent is not None
        self.helper.layout = Layout(
            Div(
                field,
                css_class="questionDiv",
                css_id= "question-"+str(question.pk),
                hidden = isHide,
            ),
            Div(Field('user'),hidden=True)
        )
        if (question.hascomment==1):
            self.fields['comment'] = forms.CharField(label="", required=False,widget=forms.Textarea(attrs={'cols': 1, 'rows': 2}))
            self.helper.layout[0].append(Field('comment',placeholder="comment",css_class='question-comment'))

    class Meta:
        model = models.Answer
        exclude = ['question','participant','interview','instrument']

AnswerFormSet = modelformset_factory(models.Answer,form=AnswerForm,extra=0,can_delete=False)
