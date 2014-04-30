from django.contrib import admin
from a.models import Term, Room, Reservation, Equipment, Board, Printer, Scanner, Note, Projector
from django import forms
from django.core.exceptions import ValidationError

admin.site.register(Reservation)
admin.site.register(Term)
admin.site.register(Scanner)
admin.site.register(Board)
admin.site.register(Note)
admin.site.register(Projector)
admin.site.register(Printer)


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'description', 'terms', 'boards']
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

    def clean_boards(self):
        boards = self.cleaned_data['boards']
        capacity = self.cleaned_data['capacity']
        found = False
        if capacity < 15 or not boards:
            for b in boards:
                found |= (b.color == 'white')
            if not found:
                raise ValidationError("A room with fewer than 15 seats must have a white board.")

        if capacity > 15 or not boards:
            for b in boards:
                found |= (b.color == 'black')
            if not found:
                raise ValidationError("A room with more than 15 seats must have a black board.")



class RoomAdmin(admin.ModelAdmin):
    filter_horizontal = ['terms']
    form = RoomForm


#class TermForm(forms.ModelForm):
#   class Meta:
#        model = Term
#        fields = ['date', 'begin_time', 'end_time']
        #exclude = ['date']

   # def clean(self):
   #     cleaned_data = super(TermForm, self).clean()
   #     begin_time = cleaned_data.get('begin_time')
   #     end_time = cleaned_data.get('end_time')

  #      if end_time < begin_time:
  #          raise forms.ValidationError("End time must not be greater than begin time")
    #    return cleaned_data


#class TermAdmin(admin.ModelAdmin):
#    form = TermForm

admin.site.register(Room, RoomAdmin)
#admin.site.register(Term, TermAdmin)

