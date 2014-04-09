from django.test import TestCase
from a.models import Room, Term, Reservation

class RoomTestCase(TestCase):
    def setUp(self):
        Room.objects.create(name="S-13", capacity=40, description='Chemistry labolatory')

    def test_animals_can_speak(self):
        chemistry = Room.objects.get(name="S-13")
        self.assertEqual(chemistry.capacity, 40)