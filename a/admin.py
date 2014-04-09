from django.contrib import admin
from a.models import User, Term, Room, Reservation, Poll, Choice


# Register your models here.
admin.site.register(Term)
#admin.site.register(Room)
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
	

admin.site.register(Poll, PollAdmin)
admin.site.register(Room, RoomAdmin)


