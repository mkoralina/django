from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime
from django.core.exceptions import ValidationError


class Term(models.Model):
    date = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return '{0}, {1} - {2}'.format(self.date, self.begin_time, self.end_time)

    class Meta:
        unique_together = ("date", "begin_time", "end_time")

    def clean(self, *args, **kwargs):
        wrong_time = False
        try:
            if self.end_time < self.begin_time:
                wrong_time = True
                raise ValidationError("End time must not be greater than begin time")
        except:
            if wrong_time:
                raise ValidationError("End time must not be greater than begin time")
            else:
                raise ValidationError("Time must be within range 00:00 - 23:59")
        super(Term, self).clean(*args, **kwargs)


# Class Room with basic info about the room to reserve
class Room(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.IntegerField()
    description = models.CharField(max_length=100)
    terms = models.ManyToManyField(Term)

    def __unicode__(self):
        return self.name


class Reservation(models.Model):
    room = models.ForeignKey(Room)
    term = models.ForeignKey(Term)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return '{0}, {1}, {2} - {3}'.format(self.user.username,
                                            self.term.date,
                                            self.term.begin_time,
                                            self.term.end_time)

    def begin_time_valid(self, begin_time, term):
        return not begin_time < term.begin_time


    def end_time_valid(self, end_time, term):
        return not end_time > term.end_time


    def prepare_term(self, begin_time, end_time, term, room):
        if begin_time > term.begin_time or end_time < term.end_time:
            if begin_time > term.begin_time:
                # we need to make w new Term with time (term.begin_time; begin_time)
                # check if the term already exists
                try:
                    new_term = Term.objects.get(date=term.date,
                                                begin_time=term.begin_time,
                                                end_time=begin_time)
                except Term.DoesNotExist:
                    new_term = Term(date=term.date, begin_time=term.begin_time,
                                    end_time=begin_time)
                    new_term.save()

                room.terms.add(new_term)

            if end_time < term.end_time:
                # check if the term already exists
                try:
                    new_term = Term.objects.get(date=term.date,
                                                begin_time=end_time,
                                                end_time=term.end_time)
                except Term.DoesNotExist:
                    new_term = Term(date=term.date, begin_time=end_time,
                                    end_time=term.end_time)
                    new_term.save()
                room.terms.add(new_term)

            #create new term between new times
            new_term = Term(date=term.date, begin_time=begin_time,
                            end_time=end_time)
            new_term.save()
            room.terms.remove(term)
            rooms = Room.objects.all()
            rooms = rooms.filter(terms=term)
            if rooms:
                pass
            else:
                term.delete()
            term = new_term

        else:
            room.terms.remove(term)
        return term


    def reserve(self, room, term, user):
        self.room = room
        self.term = term
        self.user = user
        self.save()


    def make(self, request, room_id, term_id):
        try:
            term = Term.objects.select_for_update().get(id=term_id)
            room = Room.objects.select_for_update().get(id=room_id)
        except(Term.DoesNotExist, Room.DoesNotExist):
            return render(request, 'a/make_reservation.html',
                          {'error_message': 'We are sorry, the term you wanted to '
                                            'reserve is no longer available.'})
        if request.method == "POST":
            if request.POST['begin_time'] and request.POST['end_time']:
                begin_time = request.POST['begin_time']
                end_time = request.POST['end_time']

                begin_time = datetime.strptime(begin_time, "%H:%M").time()
                end_time = datetime.strptime(end_time, "%H:%M").time()


                if not self.begin_time_valid(begin_time, term):
                    return render(request, 'a/make_reservation.html',
                                  {'error_message': 'Begin time exceeds the term'})

                if not self.end_time_valid(end_time, term):
                    return render(request, 'a/make_reservation.html',
                                  {'error_message': 'End time exceeds the term'})

                term = self.prepare_term(begin_time, end_time, term, room)

                self.reserve(room, term, request.user)

                return render(request, 'a/make_reservation.html',
                              {'begin_time': begin_time, 'end_time': end_time,
                               'room_name': room.name})

            else:
                return render(request, 'a/make_reservation.html',
                              {'error_message': 'Give both begin and end time'})
        else:
            return render(request, 'a/make_reservation.html')



class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'    


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text