from django.contrib import admin
from a.models import User, Term, Room, Reservation, Poll, Choice
from django import forms

# Register your models here.
#admin.site.register(Term)
#admin.site.register(Room)
from django.core.exceptions import ValidationError

admin.site.register(Reservation)
#admin.site.register(Choice)

#class PollAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question']

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pierwsza zakladka', {'fields': ['question']}),
        ('Druga czesc', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('question', 'pub_date', 'was_published_recently')
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question']
	

	#'classes': ['collapse'] - opcja: show/hide fieldset

class RoomAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.append('description')
        return super(Room, self).get_form(request, obj, **kwargs)


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['date', 'begin_time', 'end_time']
        #exclude = ['date']
    def clean(self):
        cleaned_data = super(TermForm, self).clean()
        begin_time = cleaned_data.get('begin_time')
        end_time = cleaned_data.get('end_time')

        if end_time < begin_time:
            raise forms.ValidationError("End time must not be greater than begin time")


class TermAdmin(admin.ModelAdmin):
    form = TermForm

#class TermAdmin(admin.ModelAdmin):
#    def validate(self):
#        begin_time = self.cleaned_data.get("begin_time")
#        end_time = self.cleaned_data.get("end_time")
#        if end_time < begin_time:
#            raise ValidationError("End_time cannot be greater than begin_time")
            #self.cleaned_data['end_time'] = begin_time
	

admin.site.register(Poll, PollAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Term, TermAdmin)

