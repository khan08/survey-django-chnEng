from django.contrib import admin
from .models import Question,Instrument,Interview,Choice
from sortedm2m_filter_horizontal_widget.forms import SortedFilteredSelectMultiple
from adminsortable2.admin import SortableInlineAdminMixin

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



# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Interview, InterviewAdmin)
admin.site.register(Choice, ChoiceAdmin)
