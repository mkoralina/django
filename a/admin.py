from django.contrib import admin
from a.models import Term, Room, Reservation
from django import forms
from django.core.exceptions import ValidationError

admin.site.register(Reservation)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'description', 'terms']

    def clean_terms(self):
        terms = self.cleaned_data['terms']
        for first in terms:
            for second in terms:
                if first.date == second.date:
                    if first.end_time <= second.begin_time or second.end_time <= first.begin_time:
                        pass
                    elif first == second:
                        pass
                    else:
                        raise ValidationError("The terms you want to add coincide.")
        return terms


class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ['terms']
    form = RoomForm


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
        return cleaned_data


class TermAdmin(admin.ModelAdmin):
    form = TermForm

admin.site.register(Room, RoomAdmin)
admin.site.register(Term, TermAdmin)

