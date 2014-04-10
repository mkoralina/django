from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client


class ReservationTestCase(TestCase):
    def setUp(self):
        self.room = Room.objects.create(name="S-13", capacity=40, description='Chemistry labolatory')
        self.term = Term.objects.create(date='2014-03-31', begin_time='10:00:00', end_time='14:00:00')
        self.user = User.objects.create_user('myuser','mymail@test.com','mypass')
        self.client = Client()

    def test_term_not_available(self):
        #room = Room.objects.get(name="S-13")
        #term = Term.objects.get(date='2014-03-31', begin_time='10:00:00', end_time='14:00:00')
        #user = User.objects.get(username = 'myuser')

        self.room.terms.add(self.term)

        self.client.login(username = 'myuser', password = 'mypass')
        response = self.client.get(reverse('a:make_reservation',
                                   args=(self.room.id,self.term.id,)))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.content  self.room.terms.all())