from django.forms.models import modelformset_factory
from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios,InlineCheckboxes
from crispy_forms.layout import Layout, Field, Div

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        question = self.instance.question
        self.choices = question.choice_set.all().order_by('sort_value')
        choice_tup = ((x.id, x) for x in self.choices)
        self.helper = FormHelper()
        self.helper.form_tag = False
        #custom layout
        if question.type==0:
            self.fields['answer'] = forms.ChoiceField(choices=(choice_tup), widget=forms.RadioSelect(), label=question,required=False)
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
                css_class="myJumbotron",
                css_id= question.pk,
                hidden = isHide,
            ),
            Div(Field('user'),hidden=True)
        )
    class Meta:
        model = models.Answer
        exclude = ['question','participant','interview','instrument']

AnswerFormSet = modelformset_factory(models.Answer,form=AnswerForm,extra=0,can_delete=False)
