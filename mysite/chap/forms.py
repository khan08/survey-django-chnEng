from django.forms.models import modelformset_factory
from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios,InlineCheckboxes
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, HTML, Div
from django.utils.safestring import mark_safe


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        question = self.instance.question
        self.choices = question.choice_set.all()
        choice_tup = ((x.id, x) for x in self.choices)
        self.helper = FormHelper()
        #self.helper.label_class = 'col-lg-12'
        #self.helper.field_class = 'col-lg-12'
        self.helper.form_tag = False

        #custom layout
        if question.type==0:
            self.fields['answer'] = forms.ChoiceField(choices=(choice_tup), widget=forms.RadioSelect(), label=question,required=False)
            field = InlineRadios('answer', choices=choice_tup, wrapper_class='radio-form',required=False)
        elif question.type==1:
            self.fields['answer'] = forms.MultipleChoiceField(choices=(choice_tup), label=question,required=False)
            field = InlineCheckboxes('answer', choices=choice_tup, wrapper_class='radio-form')
        elif question.type==2:
            self.fields['answer'] = forms.CharField(label=question,required=False)
            field = Field('answer')
        isHide = question.parent is not None
        self.helper.layout = Layout(
            Div(
                #question,
                field,
                css_class="jumbotron myJumbotron",
                css_id= question.pk,
                hidden = isHide
            ),
        )
        #self.fields['question'] = forms.(choices=(choice_tup), widget=forms.RadioInput,label='', required=False)
    class Meta:
        model = models.Answer
        exclude = ['question','user','participant','interview','instrument']


'''
AnswerFormSet = inlineformset_factory(models.Instrument,
        models.Answer,form=AnswerForm, exclude=('interview','question'),
        extra=0, can_delete=False,)
'''
AnswerFormSet = modelformset_factory(models.Answer,form=AnswerForm,extra=0,can_delete=False)
