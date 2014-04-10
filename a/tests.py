from django.test import TestCase
from a.models import Room, Term, Reservation



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