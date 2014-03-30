from django.contrib import admin
from a.models import User, Term, Room, Reservation, Poll, Choice



# Register your models here.
admin.site.register(User)
admin.site.register(Term)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Choice)

#class PollAdmin(admin.ModelAdmin):
#    fields = ['pub_date', 'question']

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Pierwsza zakladka', {'fields': ['question']}),
        ('Druga czesc', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]

#'classes': ['collapse'] - opcja: show/hide fieldset


admin.site.register(Poll, PollAdmin)