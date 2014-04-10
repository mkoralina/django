from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User


class Term(models.Model):
    date = models.DateField()
    begin_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return '{0}, {1} - {2}'.format(self.date, self.begin_time, self.end_time)

    class Meta:
        unique_together = ("date", "begin_time", "end_time")


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