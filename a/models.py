from django.db import models

# Class User with user's personal data
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    def __unicode__(self):
    	return self.first_name + " " + self.last_name

# Class Term definind available time periods to make reservation
class Term(models.Model):
	date = models.DateField()
	begin_time = models.TimeField()
	end_time = models.TimeField()
	#pass

# Class Room with basic info about the room to reserve 
class Room(models.Model):
	name = models.CharField(max_length=30)
	capacity = models.IntegerField()
	description = models.CharField(max_length=100)
	terms = models.ManyToManyField(Term)

class Reservation(models.Model):
	room = models.ForeignKey(Room)
	term = models.ForeignKey(Term)
	user = models.ForeignKey(User)

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.question
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)    

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.choice_text