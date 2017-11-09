from django.contrib import admin
from .models import Question,Instrument,Interview,Choice,Participant,Assignment,ContactLog
from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple
from adminsortable2.admin import SortableInlineAdminMixin
from django.http import HttpResponseRedirect

class QuestionInline(SortableInlineAdminMixin, admin.TabularInline):
    exclude = ('tran_date',)
    model = Question

class ChoiceInline(SortableInlineAdminMixin, admin.TabularInline):
    exclude = ('tran_date',)
    model = Choice

class InstrumentAdmin(admin.ModelAdmin):
    exclude = ('tran_date',)
    inlines = [QuestionInline,]

class QuestionAdmin(admin.ModelAdmin):
    exclude = ('tran_date',)
    inlines = [ChoiceInline, ]

class ChoiceAdmin(admin.ModelAdmin):
    exclude = ('tran_date',)

class InterviewAdmin(admin.ModelAdmin):
    exclude = ('tran_date',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'instrument':
            kwargs['widget'] = SortedFilteredSelectMultiple()
        return super(InterviewAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class ParticipantAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        """ if user clicked "edit this page", return back to main site """
        response = super(ParticipantAdmin, self).response_change(request, obj)
        if (isinstance(response, HttpResponseRedirect) and
                    request.GET.get('source') == 'main'):
            response['location'] = '/interview'

        return response

# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Assignment)
admin.site.register(ContactLog)
