from django.test import TestCase
from a.models import Room, Term, Reservation
from django.contrib.auth.models import User
import datetime
#from datetime import datetime

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

    def test_wrong_term(self):
        error = False
        try:
            term = Term.objects.create(date="2014-03-22", begin_time='14:00',
                                end_time='10:00')

            term.save()
            #term.clean()
        except:
            error = True
        self.assertTrue(error)



class ReservationTestCase(TestCase):
    def setUp(self):
        Term.objects.create(date="2014-03-22", begin_time='14:00',
                            end_time='16:00')
        Room.objects.create(name="S-13", capacity=40,
                            description='Chemistry labolatory')
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                 'johnpassword')

    def test_check_times(self):
        term = Term.objects.get(date="2014-03-22", begin_time='14:00',
                                end_time='16:00')
        begin_time = datetime.datetime.strptime('10:30', "%H:%M").time()
        end_time = datetime.datetime.strptime('17:30', "%H:%M").time()

        r = Reservation()
        self.assertFalse(r.begin_time_valid(begin_time, term))
        self.assertFalse(r.end_time_valid(end_time, term))


    def test_make_reservation(self):
        begin_time = datetime.datetime.strptime('14:30', "%H:%M").time()
        end_time = datetime.datetime.strptime('15:30', "%H:%M").time()

        term = Term.objects.get(date="2014-03-22", begin_time='14:00',
                                end_time='16:00')
        room = Room.objects.get(name="S-13", capacity=40,
                            description='Chemistry labolatory')
        #user = User.objects.get(first_name='john')
        room.terms.add(term)

        r = Reservation()
        term = r.prepare_term(begin_time, end_time, term, room)
        r.reserve(room, term, self.user)

        new_term = Term.objects.get(date="2014-03-22", begin_time='14:00',
                                end_time='14:30')
        room_available = Room.objects.filter(name="S-13", terms=new_term)
        self.assertTrue(room_available)

        new_term = Term.objects.get(date="2014-03-22", begin_time='15:30',
                                end_time='16:00')
        room_available = Room.objects.filter(name="S-13", terms=new_term)
        self.assertTrue(room_available)

