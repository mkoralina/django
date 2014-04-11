from django.test import TestCase
from a.models import Room, Term, Reservation
import datetime


class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(name="S-13", capacity=40,
                            description='Chemistry labolatory')

    def test_add_room(self):
        chemistry = Room.objects.get(name="S-13")
        self.assertEqual(chemistry.capacity, 40)

    def test_change_room(self):
        chemistry = Room.objects.get(name="S-13")
        chemistry.capacity = 60
        self.assertEqual(chemistry.capacity, 60)

    def test_delete_room(self):
        chemistry = Room.objects.get(name="S-13")
        chemistry.delete()
        chemistry = Room.objects.all().filter(name="S-13")
        self.assertFalse(chemistry.exists())


class TermTestCase(TestCase):
    def setUp(self):
        Term.objects.create(date="2014-03-22", begin_time='14:00',
                            end_time='16:00')

    def test_add_term(self):
        term = Term.objects.get(date="2014-03-22", begin_time='14:00',
                                end_time='16:00')
        self.assertEqual(term.date, datetime.date(2014, 3, 22))

    def test_add_same_term(self):
        error = 0
        try:
            Term.objects.create(date="2014-03-22", begin_time='14:00',
                                end_time='16:00')
        except:
            error = 1
        self.assertEqual(error,1)
