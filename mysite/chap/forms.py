from django.forms.models import inlineformset_factory
from . import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Field, HTML, Div
from django.utils.safestring import mark_safe


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        question = self.instance.question
        choices = question.choice_set.all()
        choice_tup = ((x.id, x) for x in choices)
        self.helper = FormHelper()
        self.helper.form_id = 'id-exampleForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.label_class = 'col-lg-12'
        self.helper.field_class = 'col-lg-12'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset(
                question,
                InlineRadios('answer', choices=choice_tup, wrapper_class='radio-form'),

            ),
            #Field('answer', autocomplete='off')
        )
        self.fields['answer'] = forms.ChoiceField(choices=(choice_tup), widget=forms.RadioSelect,label='', required=False)

    class Meta:
        model = models.Answer
        exclude = ['']
        #widgets = {'answer': forms.RadioSelect(choices=(('yes', 'yes'), ('no', 'no')))}



AnswerFormSet = inlineformset_factory(models.Instrument,
        models.Answer,form=AnswerForm, exclude=('interview','question'),
        extra=0, can_delete=False,)